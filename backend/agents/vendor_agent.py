import pandas as pd

class VendorAgent:

    def __init__(self, agent_id: str, file_path: str):
        self.agent_id = agent_id
        self.df = pd.read_excel(file_path)

        # Convert datetime columns to ISO strings so they are JSON serializable
        for col in self.df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns:
            self.df[col] = self.df[col].dt.strftime("%Y-%m-%dT%H:%M:%S")

        if "product_id" not in self.df.columns:
            self.df["product_id"] = self.df.index.astype(str)

    def _to_records(self, df: pd.DataFrame) -> list:
        # Replace NaN / Inf with None so JSON serialization never fails
        return df.where(pd.notnull(df), other=None).to_dict(orient="records")

    def handle(self, intent: str, payload: dict):

        if intent == "search_product":
            keyword = payload.get("keyword", "")
            results = self.df[
                self.df.astype(str).apply(
                    lambda row: row.str.contains(keyword, case=False).any(),
                    axis=1
                )
            ]
            return self._to_records(results)

        if intent == "get_product":
            pid = payload.get("product_id")
            result = self.df[self.df["product_id"] == str(pid)]
            return self._to_records(result)

        return []