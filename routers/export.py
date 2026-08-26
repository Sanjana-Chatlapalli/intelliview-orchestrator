from io import BytesIO

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from orchestrator.session_manager import SessionManager


router = APIRouter()

session_manager = SessionManager()


@router.get("/sessions/{session_id}/export/pdf")
def export_interview_transcript(session_id: str):
    session_data = session_manager.get_session(session_id)

    if not session_data:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    questions = session_data.get("questions_asked", [])
    answers = session_data.get("answers_provided", [])

    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(
        Paragraph("Interview Transcript", styles["Title"])
    )
    story.append(Spacer(1, 20))

    story.append(
        Paragraph(f"Session ID: {session_id}", styles["Normal"])
    )
    story.append(Spacer(1, 15))

    for index, question in enumerate(questions, start=1):
        story.append(
            Paragraph(
                f"<b>Question {index}</b>",
                styles["Heading3"]
            )
        )

        story.append(
            Paragraph(
                str(question),
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 8))

        answer_text = ""

        if index - 1 < len(answers):
            answer = answers[index - 1]

            if isinstance(answer, dict):
                answer_text = str(
                    answer.get("answer")
                    or answer.get("text")
                    or answer.get("response")
                    or answer
                )
            else:
                answer_text = str(answer)

        story.append(
            Paragraph(
                f"<b>Answer:</b> {answer_text}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 15))

    document.build(story)

    pdf_buffer.seek(0)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="interview_{session_id}.pdf"'
            )
        },
    )