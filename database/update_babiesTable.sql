BEGIN TRANSACTION;

-- Renombrar la tabla antigua
ALTER TABLE babies RENAME TO old_babies;

-- Crear la nueva tabla con la estructura actualizada
CREATE TABLE babies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    birth_date DATE NOT NULL,
    gender TEXT CHECK (gender IN ('Boy', 'Girl', 'Other')),
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Migrar los datos existentes
INSERT INTO babies (id, user_id, first_name, last_name, birth_date, gender, email, created_at)
SELECT id, user_id, 
        SUBSTR(name, 1, INSTR(name, ' ') - 1), -- Asumimos que el primer espacio divide el nombre
        SUBSTR(name, INSTR(name, ' ') + 1), 
        birth_date, gender, NULL, created_at
FROM old_babies;

-- Eliminar la tabla antigua
DROP TABLE old_babies;

COMMIT;
