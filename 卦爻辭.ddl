DROP TABLE public.卦爻辭;

CREATE TABLE public.卦爻辭 (
	id serial NOT NULL,
	本卦 varchar(2) NULL,
	卦辭 varchar(100) NULL,
	卦辭彖曰 varchar(130) NULL,
	卦辭象曰 varchar(100) NULL,
	雜卦傳 varchar(100) NULL,
	序卦傳 varchar(100) NULL,
	卦辭文言曰 varchar(100) NULL,
	初爻辭 varchar(100) NULL,
	初爻象曰 varchar(100) NULL,
	二爻辭 varchar(100) NULL,
	二爻象曰 varchar(100) NULL,
	三爻辭 varchar(100) NULL,
	三爻象曰 varchar(100) NULL,
	四爻辭 varchar(100) NULL,
	四爻象曰 varchar(100) NULL,
	五爻辭 varchar(100) NULL,
	五爻象曰 varchar(100) NULL,
	上爻辭 varchar(100) NULL,
	上爻象曰 varchar(100) NULL,
	CONSTRAINT 卦爻辭_pkey PRIMARY KEY (id)
);

drop TABLE public.六十四卦 ;
CREATE TABLE public.六十四卦(
	id serial primary key,
	本卦名 varchar(2) NULL,
	本卦組合  varchar(4) NULL,
	本卦數  varchar(6) NULL,
	錯卦名 varchar(2) NULL,
	錯卦數  varchar(6) NULL,
	綜卦名 varchar(2) NULL,
	綜卦數  varchar(6) NULL,
	複卦名 varchar(2) NULL,
	複卦數  varchar(6) NULL,
	雜卦名 varchar(2) NULL,
	雜卦數  varchar(6) NULL,
	"UTF代碼"  varchar(4) NULL
)
drop table public.卦爻辭;
create table public.卦爻辭(
        id serial primary key,
        本卦 Varchar(2) NULL,
        卦辭 Varchar(100) NULL,
        -- 爻辭 Varchar(100) NULL,
        卦辭彖曰 Varchar(100) NULL,
        卦辭象曰 Varchar(100) NULL,
        卦辭文言曰 Varchar(100) NULL,
        初爻辭 Varchar(100) NULL,
        初爻象曰 Varchar(100) NULL,
        -- 初爻彖曰 Varchar(100) NULL,
        二爻辭 Varchar(100) NULL,
        二爻象曰 Varchar(100) NULL,
        -- 二爻彖曰 Varchar(100) NULL,
        三爻辭 Varchar(100) NULL,
        三爻象曰 Varchar(100) NULL,
        -- 三爻彖曰 Varchar(100) NULL,
        四爻辭 Varchar(100) NULL,
        四爻象曰 Varchar(100) NULL,
        -- 四爻彖曰 Varchar(100) NULL,
        五爻辭 Varchar(100) NULL,
        五爻象曰 Varchar(100) NULL,
        -- 五爻彖曰 Varchar(100) NULL,
        上爻辭 Varchar(100) NULL,
        上爻象曰 Varchar(100) NULL,
        -- 上爻彖曰 Varchar(100) NULL
)
