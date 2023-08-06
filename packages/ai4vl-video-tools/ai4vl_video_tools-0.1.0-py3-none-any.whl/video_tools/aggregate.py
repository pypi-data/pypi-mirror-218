import itertools
import logging
import re
from fractions import Fraction
from pathlib import Path

import ffmpeg
from natsort import natsorted
from slugify import slugify
from tqdm import tqdm

DEFAULT_OUTPUT_FILENAME_TEMPLATE = "{study_slug}_{patient_number}-{case_number}{output_extension}"
DEFAULT_INPUT_PATH_PATTERN = r"(?P<study_name>[-\w ]+)\/(?P<patient_number>\d+)-(?P<case_number>\d+)\/(?P<stem>[-\w ]+)(?P<input_extension>\.\w+)$"

logger = logging.getLogger(__name__)


class Aggregator:
    def __init__(
        self,
        input_folder: Path,
        output_folder: Path,
        input_path_pattern: str = DEFAULT_INPUT_PATH_PATTERN,
        input_extension: str = ".mp4",
        output_extension: str = ".mp4",
        output_filename_template: str = DEFAULT_OUTPUT_FILENAME_TEMPLATE,
        seperator_frames=30,
        dry_run=False,
    ):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.input_path_pattern = input_path_pattern
        self.input_extension = input_extension
        self.output_extension = output_extension
        self.output_filename_template = output_filename_template
        self.seperator_frames = seperator_frames
        self.dry_run = dry_run
        self.seperator_path = self.output_folder / "seperator"

    def _get_input_path_re(self):
        return re.compile(self.input_path_pattern)

    def search_for_input_matches(self):
        expression = self._get_input_path_re()
        for path in self.input_folder.glob("**/*"):
            relative_path = path.relative_to(self.input_folder)
            if relative_path.suffix.lower() != self.input_extension.lower():
                continue
            if match := expression.match(relative_path.as_posix()):
                yield {"path": path, **match.groupdict()}

    def get_aggregations(self, input_matches):
        case_key = lambda match: match["case_number"]
        stem_key = lambda match: match["stem"]
        grouper = itertools.groupby(sorted(input_matches, key=case_key), case_key)
        for case_number, group in grouper:
            group = list(group)
            paths = [match["path"] for match in natsorted(group, key=stem_key)]
            yield {
                "case_number": case_number,
                "patient_number": group[0]["patient_number"],
                "study_name": group[0]["study_name"],
                "study_slug": slugify(group[0]["study_name"]),
                "snippet_count": len(paths),
                "paths": paths,
            }

    def _run_stream(self, stream):
        if self.dry_run:
            logger.info("[dry run] %s", " ".join(stream.compile()))
        else:
            out, err = stream.run(quiet=True)
            logger.debug(out)
            logger.debug(err)

    def _get_seperator_file_path(self, vary_on):
        return self.seperator_path / f"{'_'.join(str(on) for on in vary_on)}{self.input_extension}"

    def _clear_seperator_files(self):
        if self.seperator_path.exists():
            logger.info("Clearing seperator files")
            if self.dry_run:
                return
            for path in self.seperator_path.glob("*"):
                path.unlink()
            self.seperator_path.rmdir()

    def generate_output_file(self, job):
        seperator_file_path = None
        if len(job["paths"]) > 1 and self.seperator_frames:
            probe_info = ffmpeg.probe(job["paths"][0])
            v_stream = probe_info["streams"][0]
            assert v_stream["codec_type"] == "video"
            fps = Fraction(v_stream["r_frame_rate"])
            duration = float(round(self.seperator_frames / fps, 2))
            seperator_file_path = self._get_seperator_file_path(
                vary_on=[
                    "black",
                    f"{v_stream['width']}x{v_stream['height']}",
                    f"{self.seperator_frames}_at_{fps}_fps",
                ]
            )
            if not seperator_file_path.exists():
                if not self.dry_run:
                    seperator_file_path.parent.mkdir(parents=True, exist_ok=True)
                stream = (
                    ffmpeg.input(
                        f"color=black:s={v_stream['width']}x{v_stream['height']}:r={v_stream['r_frame_rate']}",
                        format="lavfi",
                    )
                    .trim(end=f"00:00:{duration}")
                    .output(seperator_file_path.as_posix())
                    .overwrite_output()
                )
                logger.info("Preparing seperator file for case %s", job["case_number"])
                self._run_stream(stream)

        logger.info("Generating case %s", job["case_number"])

        inputs = []
        for idx, path in enumerate(job["paths"]):
            inputs.append(ffmpeg.input(path.as_posix()))
            if self.seperator_frames and idx < len(job["paths"]) - 1:
                inputs.append(ffmpeg.input(seperator_file_path.as_posix()))

        stream = (
            ffmpeg.concat(*inputs)
            .output(
                (
                    self.output_folder
                    / self.output_filename_template.format(
                        study_slug=job["study_slug"],
                        patient_number=job["patient_number"],
                        case_number=job["case_number"],
                        snippet_count=job["snippet_count"],
                        output_extension=self.output_extension,
                    )
                ).as_posix(),
            )
            .overwrite_output()
        )
        self._run_stream(stream)

    def run(self):
        input_matches = self.search_for_input_matches()
        aggregations = self.get_aggregations(input_matches)
        if not self.dry_run:
            self.output_folder.mkdir(parents=True, exist_ok=True)
        for job in tqdm(list(aggregations)):
            self.generate_output_file(job)
        self._clear_seperator_files()
