SELECT
    ec."Annee",
    ec."Departement",
    md."Libelle"  AS "Nom_Departement", 
    ec."Type_cancer",
    ec."Classe_age",
    ec."Sexe",
    SUM(ec."Effectif_patients") AS "Total_Effectif_patients",
    ed."Effectif",
     (CAST(SUM(ec."Effectif_patients") AS DECIMAL) / ed."Effectif") * 100 AS "Prevalence_Pourcentage",
    COALESCE(scv_agg."Total_en_kg_agrege", 0) AS "Total_en_kg"
FROM
    "Pollution_Cancer"."Effectif_cancer" ec
INNER JOIN
    "Pollution_Cancer"."Effectif_departement" ed ON
        ec."Departement" = ed."Num_dep" AND
        ec."Annee" = ed."Annee" AND
        ec."Classe_age" = ed."Age" AND
        ec."Sexe" = ed."Sexe"
INNER JOIN
    "Pollution_Cancer"."metadata_departement" md ON 
        ec."Departement" = md."Code" 
LEFT JOIN 
    (SELECT
        scv.annee,
        scv.num_departement,
        SUM(scv."quantite_en_kg") AS "Total_en_kg_agrege"
    FROM
        "Pollution_Cancer"."Substance_cmr_vente" scv
    GROUP BY
        scv.annee,
        scv.num_departement
    ) AS scv_agg ON
        ec."Departement" = scv_agg.num_departement AND
        ec."Annee" = scv_agg.annee
WHERE
    ec."Annee" BETWEEN 2015 AND 2022
    AND ec."Classe_age" LIKE '\_T' ESCAPE '\'
    AND ec."Sexe" LIKE '\_T' ESCAPE '\'
    AND ec."Departement" = %(dept_code)s

GROUP BY
    ec."Annee",
    ec."Departement", 
    md."Libelle", 
    ec."Type_cancer",
    ec."Classe_age",
    ec."Sexe",
    ed."Effectif",
    scv_agg."Total_en_kg_agrege" 
ORDER BY
    md."Libelle" ASC,
    ec."Annee" ASC;

