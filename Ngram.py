#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# ------------------------------------------------------------------------------------
# The N-gram text splitter, special for Chinese text
#
#
# Revision history:
# 2008/12/25, Kudo Chien: Hey! It is a Christmas baby. :P
#
#
#
# Copyright 2008-2008 Kudo Chien <ckchien at gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------------
"""
import re
import string

class Ngram():
    def __init__(self, text=None, n=2, encFrom='UTF-8'):
        if not text:
            raise ValueError('Input text should not be empty.')

        self._n = n
        self._text = unicode(text, encFrom)

    def get(self):
        if len(self._text) < self._n:
            return [self._text]

        grams = []
        # split English and non-English
        text = re.sub('([^a-zA-Z0-9]*?)([a-zA-Z0-9]+)([^a-zA-Z0-9]*?)', '\\1 \\2 \\3', self._text)

        # split terms by delimiters
        delimits = string.whitespace + string.punctuation + u'，。、！：；‧〝〞‘’“”『』「」〈〉《》【】﹝﹞？'
        textList = re.split('['+delimits+']', text)

        # do ngram
        alnumRe = re.compile('^[a-zA-Z0-9]+$')
        for segment in textList:
            if not segment:
                continue
            
            if alnumRe.match(segment):
                grams.append(segment)
            else:
                lenSegment = len(segment)
                if lenSegment < self._n:
                    # Note: If you want to get the grams which length are less than n, unmark the line below
                    #grams.append(segment)
                    continue

                for i in range(lenSegment - self._n + 1):
                    grams.append(segment[i:i+self._n])

        return grams
                
    @staticmethod
    def unitTest():
        import random
        testCases = (
                '測試中文字 test. ngram 屋啦啦 中英文English',
                '貓熊到台北的第一夜「吃好睡好！」台北市立動物園今天宣布，大貓熊團團、圓圓適應良好，昨晚抵達動物園後，小寐片刻後，就從11點「吃」到凌晨3點才真正「呼呼大睡」。',
                '延宕多時、傳言滿天飛的Mark Teixeira簽約案，今天(24日)終於有了定案，而得主其實也不意外，就是已找來2位強投的洋基，Teixeira的到來幾乎可說洋基季後補強計畫全部實現。在這樁自由市場最大咖的簽約案中，Teixeira同意洋基所提之8年1億8000萬美元的價碼，平均年薪2250萬美元，只待Teixeira通過體能測試，合約就正式生效。目前為止合約細節部分尚未公佈，只知道洋基得在合約前3年付清500萬美元簽約金，而與CC Sabathia不同的是，Teixeira並無跳脫條款，但有全部的不得交易條款。在此之前，與洋基競爭Teixeira的計有紅襪、天使、國民、金鶯，而在天使日前退出競逐行列後，也只有紅襪能與洋基一搏，但紅襪的8年1億6800萬美元、平均2100萬美元提議仍比洋基少些。對於洋基先後獲得Sabathia、A. J. Burnett、Teixeira，天使總經理Tony Reagins與釀酒人老闆Mark Attanasio都異口同聲的表示：「他們(洋基)擁有龐大的資本、收入做後盾，這是其他球隊難以望其項背的；只要他們願意去做，沒有人能與其相抗衡。」甚至Attanasio還說，這是大聯盟需要設立薪資上限的時候了。洋基最近一周到底有多願意花錢？上述3人合約總值高達4億 2350萬美元。而在2008年後告別Jason Giambi(2340萬美元)、Bobby Abreu(1600萬美元)、Mike Mussina與Carl Pavano(各1100萬美元)後，所騰出的8850萬美元薪資空間有3/4花在這3人身上。若將昨天王建民500萬美元與這次Teixeira薪資算進去，已簽約的16位球員薪資已達1億8600萬美元，即便如此，洋基仍努力將來年薪資總額壓低在2億美元以下。錢的事先放一邊，重要的是Teixeira能將洋基打線提振到何種程度。Teixeira無庸置疑是專職一壘手，使得Nick Swisher被擠到外野，當然，3個位置都能守的Swisher不會有任何問題，但關鍵在於Johnny Damon、松井秀喜、Xavier Nady、Brett Gardner、Melky Cabrera的擁擠外野如何調配，以松井近年的健康狀況，擔任大部分時間的DH應是合理調度，剩下5人要搶3個位置，或許洋基會因此作出交易。因此，來年的洋基打線可能是：Damon、Derek Jeter、Teixeira、Ale Rodriguez、松井、Jorge Posada、Xavier Nady、Nick Swisher、Robinson Cano。',
                '1',
                )

        for case in testCases:
            n = random.randint(1, 5)
            objNgram = Ngram(case, n)
            gramList = objNgram.get()
            print('n = %d\nText: %s\nGrams:' % (n, case))
            print(' - '.join([gram.encode('UTF-8') for gram in gramList]))
            print('==============================\n')

if __name__ == "__main__":
    Ngram.unitTest()
