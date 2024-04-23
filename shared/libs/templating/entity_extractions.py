import os, sys, json, shutil, getpass, atexit, time, hashlib

this_dir = os.path.dirname(os.path.abspath(__file__))
shared_dir_path = os.path.join(this_dir, "shared")
cache_path = os.path.join(shared_dir_path, "dot_cache")
libs_path = os.path.join(shared_dir_path, "libs")
workspace_path = os.path.join(shared_dir_path, "workspace")

sys.path.append(libs_path)


def podcast_entity_extraction_schema():
    schema = {
        "type": "object",
        "description": "Entity extraction metadata for transcribed podcast text.",
        "properties": {
            "people": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Full name of the person."
                        },
                        "role": {
                            "type": "string",
                            "description": "Role of the person in the context of the podcast (e.g., host, guest, mentioned expert)."
                        }
                    },
                    "required": ["name"]
                },
                "description": "List of people mentioned or involved in the podcast."
            },
            "places": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "Name of the place or geographical location mentioned."
                        },
                        "context": {
                            "type": "string",
                            "description": "Description of how the place is related to the podcast content."
                        }
                    },
                    "required": ["location"]
                },
                "description": "Geographic locations mentioned in the podcast."
            },
            "things": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "thing": {
                            "type": "string",
                            "description": "Name of the object or thing mentioned."
                        },
                        "importance": {
                            "type": "string",
                            "description": "Explanation of the thing's relevance or significance in the podcast."
                        }
                    },
                    "required": ["thing"]
                },
                "description": "Objects or things mentioned in the podcast."
            },
            "relationships": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "entity1": {
                            "type": "string",
                            "description": "First entity involved in the relationship."
                        },
                        "entity2": {
                            "type": "string",
                            "description": "Second entity involved in the relationship."
                        },
                        "relationshipType": {
                            "type": "string",
                            "description": "Type or nature of the relationship (e.g., collaborator, antagonist, family)."
                        }
                    },
                    "required": ["entity1", "entity2", "relationshipType"]
                },
                "description": "Relationships between different entities mentioned in the podcast."
            },
            "identityIndicators": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "indicator": {
                            "type": "string",
                            "description": "Indicator used to suggest or reveal the identity of a party in the podcast."
                        },
                        "evidence": {
                            "type": "string",
                            "description": "Supporting information that explains the use of the indicator."
                        }
                    },
                    "required": ["indicator"]
                },
                "description": "Indicators of the identity of one or more parties involved in the podcast."
            }
        },
        "required": ["people", "places", "things", "relationships", "identityIndicators"]
    }
    return schema