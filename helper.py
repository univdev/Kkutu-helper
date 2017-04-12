# -*- coding: utf-8 -*-

import re;
import os;

def array_filter(arr):
    result = [val for val in arr if val];
    return result;

class KkutuHack:
    def __init__(self):
        dicts = os.listdir('dict');
        self.wordFilter = 0;
        self.allWord = [];
        self.genreWord = {};
        self.usingWord = {};
        self.findGenre = [];
        self.genres = [];
        self.prefixs = {};
        self.usedWord = [];

        for dict in dicts:
            file = open('dict/{}'.format(dict), 'r', encoding="UTF-8");
            genre = re.sub("\.{1}.+$", "", dict);
            self.genreWord[genre] = array_filter(file.read().split("\n"));
            self.genres.append(genre);
            file.close();

        for genre in self.genreWord:
            for word in self.genreWord[genre]:
                prefix = word[0:1];

                if prefix not in self.prefixs:
                    self.prefixs[prefix] = 1;
                else:
                    self.prefixs[prefix] += 1;

                self.allWord.append(word);

        print("\n데이터를 성공적으로 불러왔습니다.\n");

    def setting(self):
        print("원하는 단어를 얻기 위해서 필터를 설정해주세요!\n");
        print("-----------------------------------\n");
        print("1. 찾을 수 있는 단어 중 가장 긴 단어 찾기 / 받아치기 힘든 단어 순서대로 찾기\n");
        print("2. 장르 필터 켜기\n");
        print("\n0. 옵션 선택 종료\n");

        self.settingOptionQuestion();

    def settingOptionQuestion(self):
        while True:
            print("-----------------------------------\n");
            print("필터: {}\n".format("긴 단어 순서" if self.wordFilter == 0 else "받아치기 힘든 단어 순서"));
            print("장르 필터: {}\n".format(" / ".join(self.findGenre) if len(self.findGenre) else "None!"));
            choose = int(input("옵션을 선택해주세요!: "));

            if choose is 0:
                self.getMyWord();
                self.start();
                break;
            elif choose == 1:
                self.wordFilter = 1 if self.wordFilter == 0 else 0;
            elif choose == 2:
                self.viewGenreList();
                break;
            else:
                print("올바른 값을 입력해주세요!");

            self.settingOptionQuestion();

    def viewGenreList(self):
        print("\n장르를 선택해주세요!\n");
        i = 0;
        for genre in self.genres:
            i += 1;
            print("{}. {}\n".format(i, genre));
        print("0. 뒤로 가기");

        self.addGenre();

    def addGenre(self):
        choose = int(input("장르를 선택해주세요: "));

        if choose == 0:
            self.setting();
        elif choose in range(1, len(self.genres) + 1):
            self.findGenre.append(self.genres[choose-1]);
        else:
            print("잘못된 값을 입력하셨습니다. 다시 입력해주세요.");
        self.addGenre();

    def getMyWord(self):
        if len(self.findGenre) > 0:
            for genre in self.findGenre:
                for word in self.genreWord[genre]:
                    first = word[0:1];
                    if first not in self.usingWord:
                        self.usingWord[first] = [];

                    self.usingWord[first].append(word);
        else:
            for word in self.allWord:
                first = word[0:1];
                if first not in self.usingWord:
                    self.usingWord[first] = [];

                self.usingWord[first].append(word);

    def get(self, first):
        result = [];
        preAnswer = "";
        answer = "";
        defenceCnt = False;
        resultDefenceCnt = False;

        if first in self.usingWord:
            words = self.usingWord[first];
            for word in self.usingWord[first]:
                last = word[-1:];

                if word in self.usedWord:
                    continue;
                if last not in self.prefixs:
                    continue;
                if self.prefixs[last] < 1:
                    continue;

                if self.wordFilter == 0:
                    answer = word if len(answer) < len(word) else answer;
                elif self.wordFilter == 1:
                    if resultDefenceCnt is False:
                        answer = word;
                    else:
                        answer = word if resultDefenceCnt >= self.prefixs[last] else answer;

                if preAnswer != answer:
                    preAnswer = answer;
                    resultDefenceCnt = self.prefixs[last];

        if answer:
            result = [answer, len(answer), resultDefenceCnt];
            self.usedWord.append(answer);
        else:
            result = ["가능한 단어가 존재하지 않습니다", 0, 0];

        return result;

    def start(self):
        while True:
            first = str(input("검색하실 단어의 첫글자를 입력해주세요 (게임 리셋 시 0을 입력하여 초기화): "));

            if first == "0":
                os.system("cls");
                self.usedWord = [];
                continue;

            if not re.match("[가-힣]{1}", first):
                print("올바르게 입력해주세요");
                continue;

            word = self.get(first);
            print("{} (글자 수: {}) (방어단어 개수: {})\n".format(word[0], word[1], word[2]));

hack = KkutuHack();
hack.setting();
