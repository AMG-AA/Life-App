-- Tabla de usuarios
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de bebés
CREATE TABLE babies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    birth_date DATE NOT NULL,
    gender TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Tabla de hitos del desarrollo
CREATE TABLE milestones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    baby_id INTEGER NOT NULL,
    milestone TEXT NOT NULL,
    achieved_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (baby_id) REFERENCES babies (id)
);

-- Tabla de recordatorios
CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    reminder_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Tabla de registros de API
CREATE TABLE api_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    api_name TEXT NOT NULL,
    request TEXT NOT NULL,
    response TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Tabla goals (Metas)
CREATE TABLE goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificador único de la meta
    user_id INTEGER NOT NULL, -- Usuario al que pertenece la meta
    name TEXT NOT NULL, -- Nombre de la meta
    description TEXT, -- Descripción de la meta
    target_date DATE NOT NULL, -- Fecha objetivo
    budget REAL NOT NULL, -- Presupuesto asignado
    progress REAL DEFAULT 0, -- Progreso acumulado (inicia en 0)
    status TEXT DEFAULT 'En progreso', -- Estado de la meta
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación
    FOREIGN KEY (user_id) REFERENCES users (id) -- Relación con la tabla users
);

-- Tabla badges (Insignias)
CREATE TABLE badges (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificador único de la insignia
    name TEXT NOT NULL, -- Nombre de la insignia
    description TEXT NOT NULL, -- Descripción de la insignia
    icon TEXT, -- Ruta del icono de la insignia (opcional)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Fecha de creación
);

-- Tabla user_badges (Relación Usuario-Insignias)
CREATE TABLE user_badges (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificador único de la relación
    user_id INTEGER NOT NULL, -- Usuario que gana la insignia
    badge_id INTEGER NOT NULL, -- Insignia ganada
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha en la que se gana la insignia
    FOREIGN KEY (user_id) REFERENCES users (id), -- Relación con la tabla users
    FOREIGN KEY (badge_id) REFERENCES badges (id) -- Relación con la tabla badges
);

-- Tabla shared_goals (Metas Compartidas)
CREATE TABLE shared_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Identificador único de la relación
    goal_id INTEGER NOT NULL, -- Meta que se comparte
    shared_with TEXT NOT NULL, -- ID o correo del usuario con quien se comparte
    shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de compartición
    FOREIGN KEY (goal_id) REFERENCES goals (id) -- Relación con la tabla goals
);

