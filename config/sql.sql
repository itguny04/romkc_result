+-------------+-------------------------------------------------+------+-----+-------------------+----------------+
| Field       | Type                                            | Null | Key | Default           | Extra          |
+-------------+-------------------------------------------------+------+-----+-------------------+----------------+
| id          | int(11)                                         | NO   | PRI | NULL              | auto_increment |
| name        | varchar(100)                                    | NO   |     | NULL              |                |
| telno       | varchar(20)                                     | YES  |     | NULL              |                |
| email       | varchar(100)                                    | YES  |     | NULL              |                |
| area        | varchar(100)                                    | YES  |     | NULL              |                |
| description | text                                            | YES  |     | NULL              |                |
| input_time  | timestamp                                       | NO   |     | CURRENT_TIMESTAMP |                |
| status      | enum('접수완료','처리중','처리완료')            | NO   |     | 접수완료          |                |
-------------+-------------------------------------------------+------+-----+-------------------+----------------+
