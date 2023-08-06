from gandai.secrets import access_secret_version
from gandai.models import Search

import requests

class GrataWrapper:
    HEADERS = {
        "Authorization": access_secret_version("GRATA_API_TOKEN"),
        "Content-Type": "application/json",
    }

    def __name__(self):
        return "GrataWrapper"

    def find_similar(domain: str, search: Search) -> list:
        api_filters = GrataWrapper._get_api_filter(search)
        response = requests.post(
            "https://search.grata.com/api/v1/search-similar/",
            headers=GrataWrapper.HEADERS,
            json={
                "domain": domain,
                "employees_range": api_filters["employees_range"],
                "headquarters": api_filters["headquarters"],
            },
        )
        data = response.json()
        print("find_similar:", data)
        data["companies"] = data.get("results",[])  # asking grata about this
        
        return data['companies']

    def find_by_criteria(search: Search) -> dict:
        api_filters = GrataWrapper._get_api_filter(search)
        response = requests.post(
            "https://search.grata.com/api/v1/search/",
            headers=GrataWrapper.HEADERS,
            json=api_filters,
        )
        data = response.json()
        print("find_by_criteria: ", data)
        return data['companies']

    def enrich(domain: str) -> dict:
        response = requests.post(
            "https://search.grata.com/api/v1/enrich/",
            headers=GrataWrapper.HEADERS,
            json={"domain": domain},
        )
        data = response.json()
        data['linkedin'] = data.get('social_linkedin')
        data['ownership'] = data.get('ownership_status')
        return data

    def _get_api_filter(search: Search) -> dict:
        STATES = {
            "AL": "Alabama",
            "AK": "Alaska",
            "AZ": "Arizona",
            "AR": "Arkansas",
            "CA": "California",
            "CO": "Colorado",
            "CT": "Connecticut",
            "DE": "Delaware",
            "FL": "Florida",
            "GA": "Georgia",
            "HI": "Hawaii",
            "ID": "Idaho",
            "IL": "Illinois",
            "IN": "Indiana",
            "IA": "Iowa",
            "KS": "Kansas",
            "KY": "Kentucky",
            "LA": "Louisiana",
            "ME": "Maine",
            "MD": "Maryland",
            "MA": "Massachusetts",
            "MI": "Michigan",
            "MN": "Minnesota",
            "MS": "Mississippi",
            "MO": "Missouri",
            "MT": "Montana",
            "NE": "Nebraska",
            "NV": "Nevada",
            "NH": "New Hampshire",
            "NJ": "New Jersey",
            "NM": "New Mexico",
            "NY": "New York",
            "NC": "North Carolina",
            "ND": "North Dakota",
            "OH": "Ohio",
            "OK": "Oklahoma",
            "OR": "Oregon",
            "PA": "Pennsylvania",
            "RI": "Rhode Island",
            "SC": "South Carolina",
            "SD": "South Dakota",
            "TN": "Tennessee",
            "TX": "Texas",
            "UT": "Utah",
            "VT": "Vermont",
            "VA": "Virginia",
            "WA": "Washington",
            "WV": "West Virginia",
            "WI": "Wisconsin",
            "WY": "Wyoming",
        }

        COUNTRIES = {
            "USA": "United States",
            "CAN": "Canada",
            "MEX": "Mexico",
            "GBR": "United Kingdom",
        }


        def _hq_include() -> list:
            include = []
            for state in search.inclusion.get("state", []):
                # NB: API wants full state name, but product wants code
                include.append({"state": STATES[state]})
            for country in search.inclusion.get("country", []):
                include.append({"country": COUNTRIES[country]})
            return include

        def _hq_exclude() -> list:
            exclude = []
            for state in search.exclusion.get("state", []):
                exclude.append({"state": STATES[state]})
            return exclude

        return {
            "op": "any",
            "include": search.inclusion.get("keywords", []),
            "exclude": search.exclusion.get("keywords", []),
            "employees_range": search.inclusion.get("employees_range", []),
            "ownership": search.inclusion.get("ownership", ""),
            "headquarters": {
                "include": _hq_include(),
                "exclude": _hq_exclude(),
            },
        }


class SourceScrubWrapper:
    def find_similar(domain: str, search: Search) -> dict:
        pass

    def find_by_criteria(search: Search) -> dict:
        pass

    def enrich(domain: str) -> dict:
        pass
