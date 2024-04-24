CREATE TABLE IF NOT EXISTS Ventes
(
    "ID Magasin"           INTEGER,
    "ID Référence produit" TEXT,
    "Date"                 DATE,
    "Quantité"             INTEGER,
    FOREIGN KEY ("ID Référence produit") REFERENCES Produits ("Référence produit"),
    FOREIGN KEY ("ID Magasin") REFERENCES Magasins ("ID Magasin")
);

CREATE TABLE IF NOT EXISTS Produits
(   Nom                    TEXT,
    "Référence produit"    TEXT PRIMARY KEY,
    Prix                   DOUBLE PRECISION,
    Stock                  INTEGER
);

CREATE TABLE IF NOT EXISTS Magasins
(
    "ID Magasin"         INTEGER PRIMARY KEY,
    Ville                TEXT,
    "Nombre de salariés" INTEGER
);