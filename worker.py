from db import get_connection
from tools.ai_engine import generate_functional_tests
import json


def generate_functional_tests_job(job_id: int):
    """
    RQ worker entry function.
    """
    print(f"Processing job_id={job_id}")

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 1️⃣ Mark job as PROCESSING
            cursor.execute(
                """
                UPDATE scheduled_jobs
                SET status = 'PROCESSING'
                WHERE job_id = %s
                """,
                (job_id,),
            )
            conn.commit()

            # 2️⃣ Fetch framework_choice
            cursor.execute(
                """
                SELECT framework_choice
                FROM scheduled_jobs
                WHERE job_id = %s
                """,
                (job_id,),
            )
            job = cursor.fetchone()

            if not job:
                raise RuntimeError(f"Job {job_id} not found")

            framework_choice = job["framework_choice"]

            # 3️⃣ Fetch user stories
            cursor.execute(
                """
                SELECT
                    user_story_id,
                    user_story_text,
                    acceptance_criteria
                FROM user_stories
                WHERE job_id = %s
                """,
                (job_id,),
            )
            stories = cursor.fetchall()

            print(f"Fetched {len(stories)} user stories for job_id={job_id}")

            for story in stories:
                payload = {
                    "user_story": story["user_story_text"],
                    "acceptance_criteria": story["acceptance_criteria"],
                    "framework_choice": framework_choice,
                }

                # 4️⃣ Call AI engine
                result = generate_functional_tests(payload)

                # 5️⃣ Persist functional test cases
                for tc in result.test_cases:
                    cursor.execute(
                        """
                        INSERT INTO function_test_cases (
                            test_case_id,
                            job_id,
                            user_story_id,
                            result
                        )
                        VALUES (%s, %s, %s, %s::jsonb)
                        ON CONFLICT (test_case_id) DO NOTHING
                        """,
                        (
                            tc["ID"],
                            job_id,
                            story["user_story_id"],
                            json.dumps(tc),
                        ),
                    )

                # 6️⃣ Persist automation scripts
                auto = result.automation_scripts
                if auto:
                    cursor.execute(
                        """
                        INSERT INTO automation_scripts (
                            job_id,
                            user_story_id,
                            framework,
                            script
                        )
                        VALUES (%s, %s, %s, %s::jsonb)
                        ON CONFLICT (job_id, user_story_id)
                        DO UPDATE SET
                            framework = EXCLUDED.framework,
                            script = EXCLUDED.script
                        """,
                        (
                            job_id,
                            story["user_story_id"],
                            framework_choice,
                            json.dumps(auto),
                        ),
                    )

            # 7️⃣ Mark job COMPLETED
            cursor.execute(
                """
                UPDATE scheduled_jobs
                SET status = 'COMPLETED'
                WHERE job_id = %s
                """,
                (job_id,),
            )

        conn.commit()

    except Exception as e:
        conn.rollback()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE scheduled_jobs
                SET status = 'FAILED'
                WHERE job_id = %s
                """,
                (job_id,),
            )
            conn.commit()
        raise

    finally:
        conn.close()


from rq import Worker
from rq.worker import SimpleWorker
from rq_config import redis_conn

if __name__ == "__main__":
    worker = SimpleWorker(
        ["functional-test-generation"],
        connection=redis_conn
    )
    worker.work()