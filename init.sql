-- Таблица hackathon
create table hackathon (
    id uuid primary key,
    name text not null,
    task_description text not null,
    start_of_registration timestamp not null,
    end_of_registration timestamp not null,
    start_of_hack timestamp not null,
    end_of_hack timestamp not null,
    amount_money float not null,
    type text not null, -- "online" или "offline"
    created_at timestamp default current_timestamp not null,
    updated_at timestamp default current_timestamp not null
);

-- Таблица hacker
create table hacker (
    id uuid primary key,
    user_id uuid not null unique,
    name text not null,
    created_at timestamp default current_timestamp not null,
    updated_at timestamp default current_timestamp not null
);

-- Таблица role
create table role (
    id uuid primary key,
    name text not null
);

-- Таблица для связи hacker и role (one-to-many)
create table hacker_role_association (
    hacker_id uuid not null,
    role_id uuid not null,
    primary key (hacker_id, role_id),
    foreign key (hacker_id) references hacker (id) on delete cascade,
    foreign key (role_id) references role (id) on delete cascade
);

-- Таблица team
create table team (
    id uuid primary key,
    owner_uuid uuid not null,
    name text not null,
    size integer not null,
    created_at timestamp default current_timestamp not null,
    updated_at timestamp default current_timestamp not null,
    foreign key (owner_uuid) references hacker (id) on delete cascade
);

-- Таблица для связи hacker и team (many-to-many)
create table hacker_team (
    hacker_id uuid not null,
    team_id uuid not null,
    primary key (hacker_id, team_id),
    foreign key (hacker_id) references hacker (id) on delete cascade,
    foreign key (team_id) references team (id) on delete cascade
);

-- Таблица winner_solution
create table winner_solution (
    id uuid primary key,
    hack_uuid uuid not null,
    team_uuid uuid not null,
    win_money float not null,
    link_to_solution text not null,
    link_to_presentation text not null,
    can_share boolean default true not null,
    created_at timestamp default current_timestamp not null,
    updated_at timestamp default current_timestamp not null,
    foreign key (hack_uuid) references hackathon (id) on delete cascade,
    foreign key (team_uuid) references team (id) on delete cascade
);

-- Таблица для связи hackathon и team (победители)
create table hackathon_winner (
    hackathon_id uuid not null,
    team_id uuid not null,
    primary key (hackathon_id, team_id),
    foreign key (hackathon_id) references hackathon (id) on delete cascade,
    foreign key (team_id) references team (id) on delete cascade
);
