def korean_check(words)->bool:
    """
        완전한 한글음으로 이루어진 단어인지 확인
    """
    for ch in list(words.strip()):
        #공백 통과
        if ch==" ":
            continue
        #알파벳 통과 통과
        if "a" <=ch and ch<='z':
            continue
        if "A" <=ch and ch<='Z':
            continue
        #완전음 아니면 실패
        if ch<'가' or ch>'힣':
            return False

    return True

# def check_english(words)->bool:
#     """
#         알파벳이 포함되어 있는지 확인
#     """
#     for ch in list(words.strip()):
#         if ch==" ":
#             continue
#         if "a" <=ch and ch<='z':
#             return True
#         if "A" <=ch and ch<='Z':
#             return True
#     return False

def korean_to_initial(korean_word):
    """
    한글 단어를 입력받아서 초성/중성/종성을 구분하여 리턴해줍니다. 
    """
    ####################################
    # 초성 리스트. 00 ~ 18
    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    # 중성 리스트. 00 ~ 20
    JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    # 종성 리스트. 00 ~ 27 + 1(1개 없음)
    JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    ####################################
    r_lst = []
    for w in list(korean_word.strip()):
        if '가'<=w<='힣':
            ch1 = (ord(w) - ord('가'))//588
            ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
            r_lst.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
        else:
            r_lst.append([w])
    initial_list=[ch[0] for ch in r_lst]
    return "".join(initial_list)


