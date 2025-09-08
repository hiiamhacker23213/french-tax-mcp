# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance
# with the License. A copy of the License is located at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# or in the 'license' file accompanying this file. This file is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""French Tax MCP Server - Tax calculations and information retrieval."""

from typing import Dict, List

# =============================================================================
# WEBSITE URLs
# =============================================================================

# Base URLs
IMPOTS_BASE_URL = "https://www.impots.gouv.fr"
SERVICE_PUBLIC_BASE_URL = "https://www.service-public.fr"
LEGIFRANCE_BASE_URL = "https://www.legifrance.gouv.fr"

# Specific page URLs
TAX_BRACKETS_URL = "https://www.service-public.fr/particuliers/vosdroits/F1419"
IMPOTS_FORMS_BASE_URL = "/formulaires"
IMPOTS_PINEL_URL = "/particulier/questions/comment-beneficier-du-dispositif-pinel"
IMPOTS_LMNP_URL = "/particulier/questions/comment-declarer-mes-revenus-de-location-meublee"

SERVICE_PUBLIC_PARTICULIERS_URL = "/particuliers"
SERVICE_PUBLIC_TAX_SECTION_URL = "/particuliers/vosdroits/N247"
SERVICE_PUBLIC_INCOME_TAX_URL = "/particuliers/vosdroits/N10"
SERVICE_PUBLIC_PROPERTY_TAX_URL = "/particuliers/vosdroits/N13"
SERVICE_PUBLIC_DEADLINES_URL = "/particuliers/vosdroits/F34974"

LEGIFRANCE_CGI_URL = "/codes/id/LEGITEXT000006069577/"  # Code Général des Impôts
LEGIFRANCE_SEARCH_URL = "/recherche"

# =============================================================================
# TAX BRACKETS BY YEAR
# =============================================================================

TAX_BRACKETS = {
    2023: [
        {"min": 0, "max": 10777, "rate": 0},
        {"min": 10778, "max": 27478, "rate": 11},
        {"min": 27479, "max": 78570, "rate": 30},
        {"min": 78571, "max": 168994, "rate": 41},
        {"min": 168995, "max": None, "rate": 45},
    ],
    2024: [
        {"min": 0, "max": 11294, "rate": 0},
        {"min": 11295, "max": 28797, "rate": 11},
        {"min": 28798, "max": 82341, "rate": 30},
        {"min": 82342, "max": 177106, "rate": 41},
        {"min": 177107, "max": None, "rate": 45},
    ],
    2025: [
        {"min": 0, "max": 11859, "rate": 0},
        {"min": 11860, "max": 30237, "rate": 11},
        {"min": 30238, "max": 86458, "rate": 30},
        {"min": 86459, "max": 185961, "rate": 41},
        {"min": 185962, "max": None, "rate": 45},
    ],
}

# =============================================================================
# HOUSEHOLD COMPOSITION FOR QUOTIENT FAMILIAL
# =============================================================================

# Base household parts
HOUSEHOLD_PARTS_BASE = {
    "single": 1.0,
    "divorced": 1.0,
    "widowed": 1.0,
    "married": 2.0,
    "civil_union": 2.0,  # PACS
}

# Additional parts for children
HOUSEHOLD_PARTS_CHILDREN = {
    0: 0.0,
    1: 0.5,
    2: 1.0,
    3: 2.0,  # Third child and beyond: 1 full part each
}

# Additional parts for disabled dependents
HOUSEHOLD_PARTS_DISABLED = 0.5  # 0.5 parts per disabled dependent

# =============================================================================
# TAX FORMS AND DECLARATIONS
# =============================================================================

TAX_FORMS = {
    "2042": {
        "title": "Déclaration des revenus",
        "description": "Formulaire principal de déclaration des revenus des personnes physiques",
        "sections": [
            "État civil et situation de famille",
            "Traitements, salaires, pensions et rentes",
            "Revenus de capitaux mobiliers",
            "Plus-values et gains divers",
            "Revenus fonciers",
            "Charges déductibles",
            "Réductions et crédits d'impôt",
        ],
    },
    "2042-C": {
        "title": "Déclaration complémentaire",
        "description": "Formulaire complémentaire pour revenus spéciaux et réductions d'impôt",
        "sections": [
            "Revenus exceptionnels",
            "Revenus de source étrangère",
            "Réductions d'impôt spécifiques",
        ],
    },
    "2042-C-PRO": {
        "title": "Déclaration des revenus professionnels",
        "description": "Formulaire pour les revenus professionnels non salariés",
        "sections": [
            "Bénéfices industriels et commerciaux (BIC)",
            "Bénéfices non commerciaux (BNC)",
            "Bénéfices agricoles (BA)",
        ],
    },
    "2044": {
        "title": "Déclaration des revenus fonciers",
        "description": "Formulaire de déclaration des revenus fonciers (locations non meublées)",
        "sections": [
            "Propriétés rurales et urbaines",
            "Recettes brutes",
            "Frais et charges",
            "Intérêts d'emprunt",
            "Détermination du revenu ou déficit",
        ],
    },
    "2031": {
        "title": "Déclaration des résultats BIC",
        "description": "Formulaire de déclaration des bénéfices industriels et commerciaux au régime réel",
        "sections": [
            "Identification de l'entreprise",
            "Résultat fiscal",
            "Immobilisations et amortissements",
            "Provisions",
            "Plus-values et moins-values",
        ],
    },
}

# Declaration boxes for different income types
DECLARATION_BOXES = {
    "micro_enterprise": {
        "commercial": {"main": "5KO", "spouse": "5LO"},
        "services": {"main": "5KP", "spouse": "5LP"},
        "liberal": {"main": "5HQ", "spouse": "5IQ"},
    },
    "lmnp": {"micro": {"main": "5ND", "spouse": "5OD"}, "reel": {"main": "5NA", "spouse": "5OA"}},
    "versement_liberatoire": {"main": "5TA", "spouse": "5UA"},
}

# =============================================================================
# HOUSEHOLD PARTS (QUOTIENT FAMILIAL)
# =============================================================================

HOUSEHOLD_PARTS_BASE = {
    "single": 1.0,
    "divorced": 1.0,
    "separated": 1.0,
    "married": 2.0,
    "pacs": 2.0,
    "widowed": 1.0,
}

# Additional parts for children
HOUSEHOLD_PARTS_CHILDREN = {
    0: 0.0,
    1: 0.5,
    2: 1.0,
    # For 3+ children: 1.0 + (num_children - 2) * 1.0
}

# Additional parts for disabled dependents
HOUSEHOLD_PARTS_DISABLED = 0.5  # 0.5 parts per disabled dependent

# =============================================================================
# SCRAPING CONFIGURATION
# =============================================================================

# Rate limiting
DEFAULT_REQUESTS_PER_MINUTE = 10
DEFAULT_MIN_REQUEST_INTERVAL = 60 / DEFAULT_REQUESTS_PER_MINUTE  # seconds

# Timeouts and retries
DEFAULT_TIMEOUT = 10.0  # seconds
DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_RETRY_DELAY = 2.0  # seconds

# Caching
DEFAULT_CACHE_EXPIRY = 86400  # 24 hours in seconds
DEFAULT_CACHE_DIR = "~/.french_tax_mcp_cache"

# User agent for web scraping
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# =============================================================================
# TAX SCHEME MAPPINGS
# =============================================================================

TAX_SCHEMES = {
    "pinel": {
        "name": "Dispositif Pinel",
        "description": "Mécanisme de défiscalisation immobilière pour l'investissement dans un logement neuf destiné à la location",
        "url": IMPOTS_PINEL_URL,
    },
    "lmnp": {
        "name": "Location Meublée Non Professionnelle",
        "description": "Statut permettant de percevoir des revenus locatifs issus de la location meublée non professionnelle",
        "url": IMPOTS_LMNP_URL,
    },
    "lmp": {
        "name": "Loueur en Meublé Professionnel",
        "description": "Statut pour les personnes qui exercent l'activité de location meublée à titre professionnel",
        "url": IMPOTS_LMNP_URL,
    },
}

# =============================================================================
# MONTH NAMES (FRENCH)
# =============================================================================

FRENCH_MONTHS = {
    "janvier": 1,
    "jan": 1,
    "février": 2,
    "fév": 2,
    "mars": 3,
    "mar": 3,
    "avril": 4,
    "avr": 4,
    "mai": 5,
    "juin": 6,
    "jun": 6,
    "juillet": 7,
    "jul": 7,
    "août": 8,
    "aoû": 8,
    "septembre": 9,
    "sep": 9,
    "octobre": 10,
    "oct": 10,
    "novembre": 11,
    "nov": 11,
    "décembre": 12,
    "déc": 12,
}

# =============================================================================
# ERROR MESSAGES
# =============================================================================

ERROR_MESSAGES = {
    "invalid_activity_type": "Type d'activité invalide. Doit être 'commercial', 'services', ou 'liberal'.",
    "invalid_commitment_period": "Durée d'engagement invalide. Doit être 6, 9, ou 12 ans.",
    "invalid_regime": "Régime invalide. Doit être 'micro' ou 'reel'.",
    "invalid_marital_status": "Statut marital invalide.",
    "scraping_failed": "Échec de la récupération des données depuis le site web.",
    "calculation_failed": "Échec du calcul fiscal.",
    "unknown_scheme": "Dispositif fiscal inconnu.",
    "unknown_form": "Formulaire fiscal inconnu.",
}

# =============================================================================
# SUCCESS MESSAGES
# =============================================================================

SUCCESS_MESSAGES = {
    "tax_brackets_retrieved": "Tranches d'imposition récupérées avec succès",
    "scheme_details_retrieved": "Détails du dispositif récupérés avec succès",
    "form_details_retrieved": "Détails du formulaire récupérés avec succès",
    "tax_calculated": "Impôt calculé avec succès",
    "report_generated": "Rapport généré avec succès",
}
