from __future__ import annotations

import json
from typing import Any, Callable

from backend.artifacts.filesystem import ArtifactRun
from backend.pipelines.authorship import add_author_credit
from backend.pipelines.common import (
    PipelineError,
    PipelineResult,
    extract_fenced_or_raw,
    format_citations,
    format_log,
)
from backend.pipelines.html_to_pdf import (
    A4_PAGE,
    ConvertError,
    HtmlToPdfConverter,
)
from backend.providers.base import (
    ModelProviderError,
    TextGenerationProvider,
    TextGenerationRequest,
)
from backend.timing import RunTimingRecorder, measure_stage


def run_essay_html_pipeline(
    *,
    artifact_run: ArtifactRun,
    model_profile: dict[str, Any],
    model_provider: TextGenerationProvider,
    pdf_converter: HtmlToPdfConverter,
    task_text: str,
    context_bundle: str,
    output_preference: str | None,
    options: dict[str, Any] | None,
    search: dict[str, Any],
    max_output_tokens: int,
    emit_event: Callable[[str, str], None] | None = None,
    timing: RunTimingRecorder | None = None,
) -> PipelineResult:
    log_lines = [
        "Pipeline: essay_html",
        f"Output preference: {output_preference or 'pdf'}",
        "Stage: generate_source",
    ]
    system_prompt, user_prompt = build_essay_html_prompt(
        task_text=task_text,
        context_bundle=context_bundle,
        options=options or {},
        search=search,
    )
    if emit_event:
        emit_event("generate_source", "Generating essay HTML source")

    try:
        with measure_stage(timing, "provider_generation"):
            raw_output = model_provider.generate_text(
                TextGenerationRequest(
                    profile=model_profile,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    max_output_tokens=max_output_tokens,
                    temperature=0.2,
                )
            )
    except ModelProviderError as exc:
        raise PipelineError(
            exc.code,
            exc.message,
            stage="generate_source",
            log_lines=log_lines,
        ) from exc
    except Exception as exc:
        raise PipelineError(
            "provider_unavailable",
            "The model provider request failed.",
            stage="generate_source",
            log_lines=log_lines,
        ) from exc

    source = extract_fenced_or_raw(raw_output, accepted_languages={"html", "htm"})
    source = add_author_credit(source.strip()) + "\n"
    html_path = artifact_run.write_output(
        "main.html",
        source,
        kind="source",
        media_type="text/html",
    )
    log_lines.extend(["Output: output/main.html", "Stage: convert_pdf"])
    if emit_event:
        emit_event("convert_pdf", "Converting essay HTML to PDF")

    pdf_path = artifact_run.run_dir / "output" / "main.pdf"
    try:
        with measure_stage(timing, "convert_pdf"):
            convert_result = pdf_converter.convert(
                html_path=html_path,
                pdf_path=pdf_path,
                page_config=A4_PAGE,
            )
    except ConvertError as exc:
        artifact_run.write_log("convert.log", exc.log_text)
        raise PipelineError(
            "convert_failed",
            exc.message,
            stage="convert_pdf",
            log_lines=log_lines,
        ) from exc
    except Exception as exc:
        artifact_run.write_log(
            "convert.log",
            "HTML-to-PDF converter raised an unexpected error.\n",
        )
        raise PipelineError(
            "convert_failed",
            "HTML-to-PDF conversion failed.",
            stage="convert_pdf",
            log_lines=log_lines,
        ) from exc

    artifact_run.write_log("convert.log", convert_result.log_text)
    artifact_run.write_output(
        "main.pdf",
        convert_result.pdf_path.read_bytes(),
        kind="pdf",
        media_type="application/pdf",
    )
    log_lines.extend(["Convert: pdf_ok", "Output: output/main.pdf"])
    return PipelineResult(log_text=format_log(log_lines))


def build_essay_html_prompt(
    *,
    task_text: str,
    context_bundle: str,
    options: dict[str, Any],
    search: dict[str, Any],
) -> tuple[str, str]:
    system_prompt = (
        "You are an expert teaching assistant writing complete academic essay and "
        "report deliverables as self-contained HTML documents. Write in the "
        "language requested by the task. Explain technical ideas clearly, connecting "
        "each operation to its purpose and observed result. Treat supplied logs, "
        "screenshots, and deployment notes as evidence, and distinguish completed "
        "work from plans. Never invent measurements, screenshots, commands run, "
        "deployment results, URLs, costs, or references. If evidence is missing, "
        "state the limitation or mark the item as pending verification. Exclude "
        "API keys, passwords, private keys, and session tokens. Return only the "
        "requested HTML source, with no surrounding explanation."
    )
    report_guidance = (
        "Apply the following guidance when the task requests the BA3073 Mobile "
        "and Cloud Computing deployment assignment report. For unrelated essays "
        "or short smoke-test reports, follow their requested scope and length.\n"
        "1. Keep the complete assignment report within 20 A4 pages, including "
        "the title, figures, references, and appendices; aim for 10-15 pages to "
        "leave room for genuine screenshots. A shorter requested length takes "
        "precedence. Do not pad the report or add a separate empty title page. "
        "Pagination must be checked on the converted PDF by the operator; do not "
        "claim that the page limit has been verified.\n"
        "2. Use a concise title and introduction, system architecture, Task 1 "
        "local deployment and prompt improvements, Task 2 ACR/ECS deployment, "
        "Task 3 domain/HTTPS/access control, testing and troubleshooting, "
        "security and cost considerations, improvements, and references. "
        "Adapt section depth to the requested length. Explain the actual "
        "browser -> FastAPI -> Qwen request flow, SQLite metadata, persistent "
        "data/workspace mounts, and HTML-to-PDF conversion with Playwright. "
        "Explain images versus containers and host versus container ports. "
        "Do not imply that Docker Compose automatically creates a cluster.\n"
        "3. For Task 1, describe the actual local image build and Compose launch, "
        "health/UI checks, model connection and artifact generation, and the "
        "changes made to backend/pipelines/essay_html.py. Link claims to supplied "
        "evidence such as local-ui-check.txt and the local UI screenshot with "
        "the browser address bar visible.\n"
        "4. For Task 2, explain the target Linux CPU architecture, image tag and "
        "ACR push/pull, ECS container startup, persistent storage, port 14242, "
        "and the temporary security-group rule restricted to the student's "
        "own public IP. Use the supplied ecs-docker-check.txt and ECS UI "
        "screenshot with the address bar visible to support completed results.\n"
        "5. For Task 3, explain the domain's DNS A record, Nginx forwarding to "
        "127.0.0.1:14242, the TLS certificate and renewal, and an independent "
        "reverse-proxy access-control layer such as HTTP Basic Authentication. "
        "The application's BNBU login alone does not satisfy this requirement. "
        "Record the actual HTTPS domain URL and supplied evidence of successful "
        "access after authentication; include denial without credentials if "
        "tested. Explain opening ports 80/443 and closing public port 14242 "
        "after reverse-proxy verification. Do not claim these changes succeeded "
        "without evidence.\n"
        "6. For each important test, give the action, expected result, observed "
        "result, and evidence filename or figure. Explain failures, causes, and "
        "fixes only when supported by supplied records. Caption genuine supplied "
        "screenshots and refer to them from the text. Never draw a substitute "
        "screenshot or label a placeholder as proof; if an image is unavailable, "
        "write a brief explicit evidence-pending note. Keep architecture "
        "diagrams clearly separate from deployment evidence.\n"
        "7. Discuss least-privilege network access, weak built-in auth, secret "
        "handling, persistence/backups, and actual compute, storage, traffic, "
        "domain, and API cost factors without inventing prices. Propose "
        "improvements with reasons, such as stronger identity checks, updates, "
        "monitoring, backups, and automated deployment. Reference only supplied "
        "or retrieved sources with identifiable titles and URLs; omit an empty "
        "References section when no sources are available."
    )
    output_instruction = (
        "Return one complete self-contained HTML document. It must start with "
        "<!doctype html> and include <html>, <head>, and <body>, with UTF-8 "
        "charset metadata. Include all CSS inside a <style> element: use a "
        "readable serif academic print layout, approximately 11pt body text, "
        "1.4-1.5 line spacing, modest headings, careful paragraph spacing, and "
        "CSS @page { size: A4; margin: 20mm; }. Avoid fixed-height page wrappers "
        "and unnecessary forced page breaks. Keep headings with following text, "
        "use widows/orphans of at least 2, and prevent short figures, captions, "
        "and table rows from splitting where practical. Make images and diagrams "
        "fit the printable width; wrap long URLs and commands without clipping. "
        "Do not use external stylesheet links, remote images, or remote HTTP(S) "
        "assets. Embed genuine provided images only when their bytes are "
        "available. If mathematical notation is needed, include inline "
        "KaTeX-compatible markup and any needed minimal KaTeX styling inline "
        "in the document; do not fetch KaTeX from a CDN at render time. Use "
        "inline SVG or CSS for diagrams. Cite any provided web sources in a "
        "References section using ordinary HTML. Do not wrap the answer in "
        "Markdown fences."
    )
    user_prompt = "\n\n".join(
        [
            "[Assignment Task]\n" + task_text.strip(),
            "[Prepared Context]\n" + context_bundle.strip(),
            "[Search Citations]\n" + format_citations(search),
            "[Options]\n" + json.dumps(options, sort_keys=True),
            "[BA3073 Report Guidance]\n" + report_guidance,
            "[Output Contract]\n" + output_instruction,
        ]
    )
    return system_prompt, user_prompt
