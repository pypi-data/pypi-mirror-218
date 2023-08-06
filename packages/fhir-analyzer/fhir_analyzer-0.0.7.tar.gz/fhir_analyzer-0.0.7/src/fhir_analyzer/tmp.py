import sys
from fhir_analyzer.fhirstore import Fhirstore
from fhir_analyzer.feature_selector import FeatureSelector

from fhir_analyzer.patient_similarity.patsim import Patsim
import json
import os

ex = {
    "resourceType": "Observation",
    "id": "f9c5653f-a8c8-4c07-89d9-e7e66dcce4c8",
    "status": "final",
    "category": [
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "vital-signs",
                    "display": "vital-signs",
                }
            ]
        }
    ],
    "code": {
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "55284-4",
                "display": "Blood Pressure",
            }
        ],
        "text": "Blood Pressure",
    },
    "subject": {"reference": "urn:uuid:67816396-e325-496d-a6ec-c047756b7ce4"},
    "encounter": {"reference": "urn:uuid:3c16aa88-87cb-4d82-a640-89b52750f543"},
    "effectiveDateTime": "2009-12-20T22:52:53-05:00",
    "issued": "2009-12-20T22:52:53.991-05:00",
    "component": [
        {
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8462-4",
                        "display": "Diastolic Blood Pressure",
                    }
                ],
                "text": "Diastolic Blood Pressure",
            },
            "valueQuantity": {
                "value": 83.85333428922644,
                "unit": "mm[Hg]",
                "system": "http://unitsofmeasure.org",
                "code": "mm[Hg]",
            },
        },
        {
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8480-6",
                        "display": "Systolic Blood Pressure",
                    }
                ],
                "text": "Systolic Blood Pressure",
            },
            "valueQuantity": {
                "value": 116.43901482684636,
                "unit": "mm[Hg]",
                "system": "http://unitsofmeasure.org",
                "code": "mm[Hg]",
            },
        },
    ],
}

patsim = Patsim()
fhs = Fhirstore()
with open("../data/bundles/test_bundle_002.json", "r") as f:
    bundle = json.load(f)
    patsim.add_bundle(bundle)
    fhs.add_bundle(bundle)

with open("../data/bundles/test_bundle_001.json", "r") as f:
    bundle = json.load(f)
    patsim.add_bundle(bundle)
    fhs.add_bundle(bundle)

with open(
    "/Users/tillrostalski/Git/old_whipple/oldwebapp/server/data/synthea_1/synthea_sample_data_fhir_r4_sep2019/Floyd420_Jerde200_0979f4fe-08c5-414e-ba1c-6ccf852bcce4.json",
    "r",
) as f:
    bundle = json.load(f)
    patsim.add_bundle(bundle)
    fhs.add_bundle(bundle)


fs = FeatureSelector(fhirstore=fhs)
fs._add_feature("he", "categorical_string", ["Patient"], {"name": ["name.given"]})

patsim.add_categorical_feature(
    name="Diagnoses",
    resource_types=["Condition"],
    target_paths=["code.coding.display"],
)

patsim.add_categorical_feature(
    name="Insurance",
    resource_types=["Claim"],
    target_paths=["insurance.coverage.display"],
)

patsim.add_categorical_feature(
    name="Name",
    resource_types=["Patient"],
    target_paths=["name.given"],
)

patsim.add_numerical_feature(
    name="Age",
    resource_types=["Patient"],
    target_paths=["age"],
)

fs = FeatureSelector(fhirstore=fhs)
fs.add_feature(
    name="Name",
    resource_types=["Patient"],
    target_paths=["name.given"],
)

fs.add_feature(
    name="Diagnoses",
    resource_types=["Condition"],
    target_paths=["code.coding.display"],
)


print(fs._patient_features)
print(fs.feature_df)
