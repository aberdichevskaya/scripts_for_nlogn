Для того, чтобы она работал скрипт для звёздочек (add_stars), нужно:
1) создать отдельную группу типа "начинающие питон задачи со звёздочкой", она должна быть пустая. контест со звёздочкой должен быть открыт только для этой группы
2) В 18-й строке нужно добавить номер группы со звёздочкой во множество STARS_GROUPS
3) когда начинается контест, запускаешь этот скрипт, он там просит ввести название контестов


Суть работы в том, что по ходу дела она отслеживает детей, которые всё решили, и добавляет их в эту отдельную группу => они начинают видеть контест. После окончания базоваго контеста контест со звёздочкой открывается для всех групп, для которых был основной контест, а группу для звёздочек очищается.
