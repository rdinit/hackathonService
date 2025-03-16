-- Таблица hacker
create table hacker (
    id uuid primary key,
    user_id uuid not null,
    name text not null,
    created_at timestamp default current_timestamp not null,
    updated_at timestamp default current_timestamp not null,

    CONSTRAINT uq_hacker_user_id UNIQUE (user_id)
);

-- Таблица для связи hacker и role (one-to-many)
create table hacker_role_association (
    hacker_id uuid not null,
    role text not null check (role in (select ('admin', 'backend', 'frontend', 'ml', 'designer'))),
    primary key (hacker_id, role_id),
    foreign key (hacker_id) references hacker (id) on delete cascade
);

-- Таблица team
create table team (
    id uuid primary key,
    owner_id uuid not null,
    name text not null,
    max_size integer not null check (max_size > 0),
    created_at timestamp default current_timestamp not null,
    updated_at timestamp default current_timestamp not null,
    foreign key (owner_id) references hacker (id) on delete cascade,

    CONSTRAINT uq_team_owner_id_name UNIQUE (owner_id, name)
);

-- Таблица для связи hacker и team (many-to-many)
create table hacker_team_association (
    hacker_id uuid not null,
    team_id uuid not null,
    primary key (hacker_id, team_id),
    foreign key (hacker_id) references hacker (id) on delete cascade,
    foreign key (team_id) references team (id) on delete cascade
);

-- Таблица hackathon
create table hackathon (
    id uuid primary key,
    name text not null,
    task_description text,
    start_of_registration timestamp with time zone,
    end_of_registration timestamp with time zone,
    start_of_hack timestamp with time zone not null,
    end_of_hack timestamp with time zone,
    amount_money float,
    type text, -- "online" или "offline"
    created_at timestamp default current_timestamp not null,
    updated_at timestamp default current_timestamp not null,

    CONSTRAINT uq_hackathon_name_start UNIQUE (name, start_of_hack)
);


-- Таблица winner_solution
create table winner_solution (
    id uuid primary key,
    win_money float not null,
    link_to_solution text not null,
    link_to_presentation text not null,
    can_share boolean default true not null,
    hackathon_id uuid not null,
    team_id uuid not null,
    foreign key (hackathon_id) references hackathon (id) on delete cascade,
    foreign key (team_id) references team (id) on delete cascade,
    created_at timestamp default current_timestamp not null,
    updated_at timestamp default current_timestamp not null,

    CONSTRAINT uq_winner_solution_hackathon_id_team_id UNIQUE (hackathon_id, team_id)
);
