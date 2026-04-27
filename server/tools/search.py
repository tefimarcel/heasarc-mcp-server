from astroquery.heasarc import Heasarc
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import astropy.units as u
from server.utils.missions import MISSIONS, SUPPORTED_MISSIONS


def resolve_object(name: str) -> dict:
    """Resolve an astronomical object name to RA/Dec coordinates via SIMBAD."""
    try:
        result = Simbad.query_object(name)
        if result is None:
            return {"error": f"Object '{name}' not found in SIMBAD"}

        colnames = result.colnames
        ra_col  = "ra"  if "ra"  in colnames else "RA"
        dec_col = "dec" if "dec" in colnames else "DEC"

        ra  = result[ra_col][0]
        dec = result[dec_col][0]

        return {
            "object": name,
            "ra": float(ra),
            "dec": float(dec),
            "message": f"{name} → RA: {ra}, Dec: {dec}"
        }
    except Exception as e:
        return {"error": str(e)}


def search_observations(
    object_name: str,
    mission: str = "all",
    min_exposure_ks: float = 0.0,
    max_results: int = 100
) -> dict:
    """Search HEASARC for observations of a given astronomical object."""

    missions_to_search = (
        SUPPORTED_MISSIONS if mission.lower() == "all"
        else [mission] if mission in MISSIONS
        else None
    )

    if missions_to_search is None:
        return {"error": f"Mission '{mission}' not supported. Options: {SUPPORTED_MISSIONS}"}

    # Resolve object name to coordinates
    resolved = resolve_object(object_name)
    if "error" in resolved:
        return {"error": f"Could not resolve object '{object_name}': {resolved['error']}"}

    coords = SkyCoord(ra=resolved["ra"], dec=resolved["dec"], unit="deg")

    heasarc = Heasarc()
    results = {}

    for m in missions_to_search:
        config = MISSIONS[m]
        try:
            table = heasarc.query_region(
                coords,
                catalog=config["table"],
                radius=1 * u.deg,
                maxrec=max_results
            )

            if table is None or len(table) == 0:
                results[m] = []
                continue

            id_col  = config["id_column"]
            exp_col = config["exposure_column"]
            extra_cols = config.get("extra_columns", [])

            obs_list = []
            for row in table:
                obs_id = str(row[id_col])

                try:
                    exposure_ks = float(row[exp_col]) / 1000.0 if exp_col else 0.0
                except Exception:
                    exposure_ks = 0.0

                if exposure_ks < min_exposure_ks:
                    continue

                obs = {
                    "obs_id": obs_id,
                    "exposure_ks": round(exposure_ks, 1),
                    "mission": m,
                }

                # Add mission-specific extra columns
                for col in extra_cols:
                    if col in table.colnames:
                        obs[col] = str(row[col])

                obs_list.append(obs)

            results[m] = obs_list

        except Exception as e:
            results[m] = {"error": str(e)}

    return results
