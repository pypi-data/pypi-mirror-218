# std

a standard library for algorithms:

## multi-language segmenter 
pip install std.algorithm  
python  

from std.nlp.segment.cn import split  
split('结婚的和尚未结婚的确实在场地上散步。')  #['结婚', '的', '和', '尚未', '结婚', '的', '确实', '在', '场地', '上', '散步', '。']  

from std.nlp.segment.jp import split  
split('の出力と前記第3のゲート回路34-oの出力とを入力するアンドゲート回路35を備え、') #['の', '出力', 'と', '前記', '第', '3', 'の', 'ゲート', '回路', '34', '-', 'o', 'の', '出力', 'と', 'を', '入力', 'する', 'アンド', 'ゲート', '回路', '35', 'を', '備え', '、']  

from std.nlp.segment.en import split   
split('who are you?') #['who ', 'are ', 'you', '?']  

