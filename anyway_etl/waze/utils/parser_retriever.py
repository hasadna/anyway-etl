import pandas as pd
from anyway.models import WazeAlert, WazeTrafficJams


def __convert_to_bool(value):
    if isinstance(value, bool):
        return value
    else:
        return str(value).lower() in ("yes", "true", "t", "1")


def _parse_alerts(rows):
    alerts_df = pd.json_normalize(rows)

    alerts_df["created_at"] = pd.to_datetime(alerts_df["pubMillis"], unit="ms")

    alerts_df.rename(
        {
            "location.x": "longitude",
            "location.y": "latitude",
            "nThumbsUp": "number_thumbs_up",
            "reportRating": "report_rating",
            "reportDescription": "report_description",
            "reportByMunicipalityUser": "report_by_municipality_user",
            "jamUuid": "jam_uuid",
            "type": "alert_type",
            "subtype": "alert_subtype",
            "roadType": "road_type",
        },
        axis=1,
        inplace=True,
    )

    alerts_df["geom"] = alerts_df.apply(
        lambda row: "POINT({} {})".format(row["longitude"], row["latitude"]), axis=1
    )

    alerts_df["road_type"] = int(alerts_df["road_type"].fillna(-1)[0])
    alerts_df["number_thumbs_up"] = int(alerts_df.get("number_thumbs_up", 0))
    alerts_df["report_by_municipality_user"] = __convert_to_bool(
        alerts_df.get("report_by_municipality_user", False)
    )

    alerts_df.drop(["country", "pubMillis"], axis=1, inplace=True, errors="ignore")

    for key in alerts_df.keys():
        if alerts_df[key] is None or key not in [
            field.name for field in WazeAlert.__table__.columns
        ]:
            alerts_df.drop([key], axis=1, inplace=True)

    return alerts_df.to_dict("records")


def __parse_jams(rows):
    jams_df = pd.json_normalize(rows)
    jams_df["created_at"] = pd.to_datetime(jams_df["pubMillis"], unit="ms")
    jams_df["geom"] = jams_df["line"].apply(
        lambda l: "LINESTRING({})".format(
            ",".join(["{} {}".format(nz["x"], nz["y"]) for nz in l])
        )
    )
    jams_df["line"] = jams_df["line"].apply(str)
    jams_df["segments"] = jams_df["segments"].apply(str)
    jams_df["turnType"] = jams_df["roadType"].fillna(-1)
    jams_df.drop(["country", "pubMillis"], axis=1, inplace=True)
    jams_df.rename(
        {
            "speedKMH": "speed_kmh",
            "turnType": "turn_type",
            "roadType": "road_type",
            "endNode": "end_node",
            "blockingAlertUuid": "blocking_alert_uuid",
            "startNode": "start_node",
        },
        axis=1,
        inplace=True,
    )

    for key in jams_df.keys():
        if jams_df[key] is None or key not in [
            field.name for field in WazeTrafficJams.__table__.columns
        ]:
            jams_df.drop([key], axis=1, inplace=True)

    return jams_df.to_dict("records")


class ParserRetriever:
    def __init__(self):
        self.__parsers = {"alerts": _parse_alerts, "jams": __parse_jams}

    def get_parser(self, field: str):
        return self.__parsers.get(field, lambda rows: rows)