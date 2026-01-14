select database();
CREATE TABLE RollerChorderDatabaseTable (
	telegram_id varchar(190) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL ,
	qr_hash_code varchar(190) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
	last_link varchar(190) CHARACTER SET utf8 COLLATE utf8_general_ci ,
	user_state varchar(190) CHARACTER SET utf8 COLLATE utf8_general_ci ,
	first_signin timestamp DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (telegram_id),
    UNIQUE (qr_hash_code)
	);
	
22e1ec9e965f16c5dc4481652d162f3


0101dd85b5fa1f9bb7e38c32da4706aee65e75c3312706c1b78f3c56fb7db693
0101dd85b5fa1f9bb7e38c32da4706aee65e75c3312706c1b78f3c56fb7db693

3dc505b80aa4dc0ef5bcf3527abd0c94bec91a97c3093c67756f80ab650eb807