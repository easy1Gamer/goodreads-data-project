drop table review_data;
drop table book_data;

create table book_data
(
    site_index       int unique not null,
    work_id          text       not null,
    book_name        text       not null,
    author           text,
    rating           numeric(3, 2),
    nb_ratings       int,
    nb_reviews       int,
    nb_5_stars       int,
    nb_4_stars       int,
    nb_3_stars       int,
    nb_2_stars       int,
    nb_1_stars       int,
    genres           text array,
    series_name      text,
    description      text,
    nb_pages         int,
    publication_date date,
    awards           text array,
    constraint book_pk primary key (site_index)
);

create table review_data
(
    id            serial primary key,
    book_index    int not null,
    review_rating int,
    review        text,
    constraint fk_review foreign key (book_index) references book_data (site_index)
);


