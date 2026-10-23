import json
import pandas as pd


def load_uploaded_logs(uploaded_files):

    events = []

    if not uploaded_files:
        return events

    for file in uploaded_files:

        try:

            # JSON
            if file.name.lower().endswith(".json"):

                data = json.load(file)

                if isinstance(data, list):
                    events.extend(data)
                else:
                    events.append(data)

            # CSV
            elif file.name.lower().endswith(".csv"):

                df = pd.read_csv(file)

                events.extend(
                    df.to_dict(
                        orient="records"
                    )
                )

            # TXT
            elif file.name.lower().endswith(".txt"):

                content = file.read().decode(
                    "utf-8",
                    errors="ignore"
                )

                events.append({
                    "source": "txt",
                    "filename": file.name,
                    "content": content
                })

            # LOG
            elif file.name.lower().endswith(".log"):

                content = file.read().decode(
                    "utf-8",
                    errors="ignore"
                )

                events.append({
                    "source": "log",
                    "filename": file.name,
                    "content": content
                })

        except Exception as e:

            print(
                f"Error processing {file.name}: {e}"
            )

    return events