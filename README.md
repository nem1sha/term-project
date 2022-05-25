# term-project
### Поиск контуров на картинке (с камеры) и сохранение контуров в векторное изображение svg
< Перед вами программа для поиска контуров на картинке и с камеры и сохранение контуров в векторное изображение svg
Перед началом работы с программой советую Вам ознакомится с инструкцией. 
### Инструкция
<Программа имеет три варианта работы:
1)	‘Поиск контура на картинке’. Вам предстоит ввести значения для фильтра вручную:
*’h1’ – цветовой фон для минимальных значений
*’s1’ – освещение для минимальных значений
*’v1’ – яркость для минимальных значений

*’h2’ – цветовой фон для максимальных значений

*’s2’ – освещение для максимальных значений

*’v2’ – яркость для минимальных значений

Затем программа фильтрует картинку и рисует контуры. 
2)	‘Поиск контура на картинке’. Вам откроется окно, в котором, изменяя положения бегунков, вы настраиваете значения фильтра, для наилучшего обнаружения контура на изображении (совет: начинать работать с бегунками по порядку, прописанном в первом варианте). Затем программа фильтрует картинку и рисует контуры для неё. 

3)	‘Поиск контура на видео’.  Вам откроется окно, в котором, изменяя положения бегунков, вы настраиваете значения фильтра для видео с вашей камеры. Затем программа делает фотографию, фильтрует её и рисует контуры для неё.

***

###!!! Очень важно
Eсли вы хотите, чтобы программа работала с картинкой, то необходимо написать путь для неё в конструкторе класса Camera (self.img = ‘путь к картинке’)
