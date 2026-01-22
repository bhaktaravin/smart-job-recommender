import io
import os
import uuid
import pytest
import requests

pytestmark = pytest.mark.integration

BASE = "http://localhost:8000"


def _make_minimal_pdf_bytes():
    pdf = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT /F1 24 Tf 72 712 Td (Hello) Tj ET\nendstream\nendobj\n5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\nxref\n0 6\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000123 00000 n \n0000000220 00000 n \n0000000300 00000 n \ntrailer\n<< /Root 1 0 R /Size 6 >>\nstartxref\n380\n%%EOF\n"
    return pdf


@pytest.mark.skipif(
    os.getenv("CI") == "true",
    reason="Profile upload test uses DB and may be environment-specific; skip on CI unless configured",
)
def test_profiles_upload():
    try:
        import psycopg2
    except Exception:
        pytest.skip("psycopg2 not installed; skipping DB-backed profile upload test")

    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port=5432)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user_profiles (
                id SERIAL PRIMARY KEY,
                name TEXT,
                email TEXT UNIQUE,
                text TEXT
            )
            """
        )
        conn.commit()

        test_email = f"test+{uuid.uuid4()}@example.com"
        cur.execute(
            "INSERT INTO user_profiles (name, email, text) VALUES (%s, %s, %s) RETURNING id",
            ("Test User", test_email, ""),
        )
        user_id = cur.fetchone()[0]
        conn.commit()

        pdf_bytes = _make_minimal_pdf_bytes()
        files = {"file": ("resume.pdf", io.BytesIO(pdf_bytes), "application/pdf")}
        r = requests.post(f"{BASE}/profiles/upload_resume/{user_id}", files=files)
        assert r.status_code == 200
        body = r.json()
        assert "message" in body or "text_snippet" in body

        cur.execute("SELECT text FROM user_profiles WHERE id = %s", (user_id,))
        text = cur.fetchone()[0]
        assert text is not None
    finally:
        cur.execute("DELETE FROM user_profiles WHERE email LIKE %s OR name=%s", ("test+%", "Test User"))
        conn.commit()
        cur.close()
        conn.close()
