---
source: "https://muki.tw/obsidian-template-daily-weekly-journal-tasks/"
title: "用 Obsidian 設計自己的週計畫與週誌 – MUKI space*"
fetched_at: "2026-10-06 12:50"
---

📄 用 Obsidian 設計自己的週計畫與週誌.md

## 前言

會想用 Obsidian 就是看中他的高自由度以及高客製化。而我有一本實體的工作手帳，所以想把手帳版面直接搬到 Obsidian，以下是我的需求：

  * 可以寫 Life Log (生活記錄片段)
  * 可以規劃並控管我的待辦事項
  * 格式是一週一頁



最後我的版面大致如下，有興趣的朋友可以繼續往下看，我會跟大家介紹我使用的 plugins，以及我的設定檔。

## 安裝 Plugins

我們要安裝兩個 Plugins：

  * [Periodic Notes](https://github.com/liamcain/obsidian-periodic-notes) (可以產生 Daily，Weekly，Monthly，Quarterly，Yearly 多種日誌計畫的版面)
  * [Tasks](https://github.com/obsidian-tasks-group/obsidian-tasks) (非常強大的待辦管理套件，真心推薦必裝)



提醒：請先安裝好這兩個 Plugins 再往下設定唷！

Obsidian 是直接跟放上 github 上的 plugins 做整合，所以我們可以直接在 Obsidian 的設定裡，安裝並啟用這些 plugins

▼ 點選左下角的「設定圖案」-> 「Community plugins」->「Browse」，就能看到所有在 github 上的 Obsidian plugins

▼ 搜尋剛剛提到的兩個 plugins：[Periodic Notes](https://github.com/liamcain/obsidian-periodic-notes) 以及 [Tasks](https://github.com/obsidian-tasks-group/obsidian-tasks)，安裝後記得選擇「Enabled」啟用就可以了。

有的 plugin 名字可能會長得很像，這時候可以對照 github 的作者名稱和描述來確認唷！

## 設定 Periodic Notes

▼ Periodic Notes 可以產生多個版面，將你想要產生的格式開啟，就可以做設定了

建議選一個版面就好

為了避免造成混亂，初期建議大家選擇一個版面就好，用不到的記得關閉。  
未來如果熟悉了 Obsidian 系統，可再視情況選擇多個版面。

### Format

檔案格式是「日期 + 時間」，Format 欄位可以讓我們設定格式，他還有預覽功能，能直接看到格式的範例文字，如果寫錯能隨時調整。

我以前有用他的 Daily Notes，我當時的設計是想用「資料夾 + 檔案」的格式，資料夾名稱利用年份分類，畢竟一年有 365 天，如果沒用資料夾分類，怕檔案拖太長 XD。

因此我用的 Daily Notes 的 Format 設定為 `gggg/YYYY.MM.DD`，「`/`」表示分層資料夾。

▼ 以 4 月 12 為例，當我新建了一個 Daily Note，他就會自動幫我放到 2024 的資料夾底下，檔案名稱為 2024.04.12.md

▼ 但我現在用的是 Weekly Notes，所以我會關閉 Daily Notes，打開 Weekly Notes

我的 Weekly Format 格式為 `gggg.MM.[Week]w`，以第 15 週為例，檔案名稱為 2024.04.Week15.md

### Note Template

我們還能整合 Obsidian 的 Template 功能，設計自己的 template，注意要輸入完整的 template 路徑，包含檔名，才能正確抓到該 template。路徑名稱如果有大小寫或空格，都必須要如實輸入唷。

### Note Folder

最後設定新增的檔案要放在哪裡？一樣是填寫完整的資料夾路徑即可

## 製作 Template

如果你已經設定好 template 路徑，我們就來製作 template 吧。

我要做的是週計畫，因此我希望看到這週的檔案筆記，就能知道該筆記的日期範圍，畢竟「15 週」這資訊不太直覺。所以我會建一個 YAML 為：

  * `start_date：{{monday:YYYY-MM-DD}}`
  * `end_date：{{friday:YYYY-MM-DD}}`



注意

這個有一個我無法處理的小 bug XD，套件預設是以禮拜天為當週起始日，而非禮拜一。我自己是習慣禮拜一作為起始日，所以我如果設定 `end_date` 為 `{{sunday:YYYY-MM-DD}}`，日期就會有誤。  
  
雖然套件作者表示，會依照我們在 obsidian 的設定，自動調整起始日為週一 / 週日，但我實測是失敗的，所以我的 `end_date` 就改成禮拜五了。  
  
但我原本就是拿來記錄工作的待辦事項，沒有六日也沒差，所以我的週計畫只有週一到週五。

接下來文章分作兩部分，一個是 Life Log，讓我自由發揮；一個是 Tasks，搭配剛剛安裝的 Task 套件，自動顯示我當天要處理的待辦事項。

▼ 以下是完整的檔案語法，可以直接複製到自己的 markdown 再做微調
    
    
    ---
    start_date：{{monday:YYYY-MM-DD}}
    end_date: {{friday:YYYY-MM-DD}}
    ---
    
    ## {{ monday:MM.DD }} MON
    
    **Life Log**
    
    **Tasks**
    
    ```tasks
    hide postpone button
    hide backlink
    hide start date
    starts on or before {{monday:YYYY-MM-DD}}
    due on or after {{monday:YYYY-MM-DD}}
    ```
    
    ## {{ tuesday:MM.DD }} TUE
    
    **Life Log**
    
    **Tasks**
    
    ```tasks
    hide postpone button
    hide backlink
    hide start date
    starts on or before {{tuesday:YYYY-MM-DD}}
    due on or after {{tuesday:YYYY-MM-DD}}
    ```
    
    ## {{ wednesday:MM.DD }} WED
    
    **Life Log**
    
    **Tasks**
    
    ```tasks
    hide postpone button
    hide backlink
    hide start date
    starts on or before {{wednesday:YYYY-MM-DD}}
    due on or after {{wednesday:YYYY-MM-DD}}
    ```
    
    ## {{ thursday:MM.DD }} THU
    
    **Life Log**
    
    **Tasks**
    
    ```tasks
    hide postpone button
    hide backlink
    hide start date
    starts on or before {{thursday:YYYY-MM-DD}}
    due on or after {{thursday:YYYY-MM-DD}}
    ```
    
    ## {{ friday:MM.DD }} FRI
    
    **Life Log**
    
    **Tasks**
    
    ```tasks
    hide postpone button
    hide backlink
    hide start date
    starts on or before {{friday:YYYY-MM-DD}}
    due on or after {{friday:YYYY-MM-DD}}
    ```
    

tasks 裡面的語法，我的處理是隱藏一些不想要的資訊，詳細的設定可以參考 Hiding / Showing Elements

[](https://publish.obsidian.md/tasks/Queries/Layout "Layout - Tasks User Guide - Obsidian Publish")

Layout - Tasks User Guide - Obsidian Publish

Layout - Tasks User Guide - Powered by Obsidian Publish.

再來篩選要出現的任務項目，我的篩選條件如下：

  1. 顯示任務開始日期為今天之前 (包含今天)  
語法：starts on or before 日期  
作用：昨天以前沒做完的任務，今天才會繼續顯示，提醒我們要接著處理。
  2. 顯示任務預計的結束日期是今天之後 (包含今天)  
語法：due on or after 日期  
作用：用來看我們排程的任務；假設今天的工作都做完了，就可以看明後天要做什麼任務，方便復盤。



語法錯誤？

如果你在 template.md 使用 preview mode，應該會看到 tasks 的語法有錯，但這是正常的，因為 template 的日期都是變數，tasks 沒辦法根據變數去篩選資料，因此會報錯。  
  
但只要我們透過 template 建立新的筆記取得正確日期後，tasks 的語法就會正常運作了，如果是非 template 的筆記取得資料時發生了問題，歡迎留言詢問，我們可以一起討論處理。

## 製作待辦清單的筆記頁面

做好 template 也串好 task 語法了，那麼，task 從哪裡來呢？

我習慣做一個專門紀錄 task 的筆記頁面，把所有想到的待辦事項都寫在裡面，再利用剛剛的 Periodic Notes 的週計畫 Template 幫我們分類即可。

在 Obsidian 的筆記頁面輸入 /tasks 就可以開啟 task 套件的相關指令，這邊就不再多說使用方法了，相信有用過 Obsidian 套件的朋友都很熟悉這套操作模式，不熟的朋友可以再自行搜尋該套件的使用方法。他們的官方也有非常詳細的文件可供參考：

[](https://publish.obsidian.md/tasks "Introduction - Tasks User Guide - Obsidian Publish")

Introduction - Tasks User Guide - Obsidian Publish

Introduction - Tasks User Guide - Powered by Obsidian Publish.

▼ 我沒有特別分類，想到什麼就寫什麼

最後再透過 Periodic Notes 新增你的 Daily / Weekly Note，就能自動將待辦事項顯示到對應的日期囉。

▼ 如果你跟我一樣用的是 Weekly Note，那麼會在左側側邊欄看到一個日曆的圖案，滑鼠移過會出現「Open this Week」，點擊後就會自動帶出當週的日期了。

▼ 點選「Open this week」後，會自動產生一份當週的文件，裡面有對應的日期和任務

如果你用的是 Daily Notes

如果你有打開 Daily Notes，那麼左側側邊欄的 icon 會變成「open today」，你的設定就必須都寫在 Daily Notes 的欄位才有作用。

## 完整的 Vault 資料夾

最近陸續有朋友詢問 Obsidian 的設定問題，很多人都是同時把 Daily Notes 和 Weekly Notes 打開，造成 template 讀取失敗。

所以我做了一份只有「Weekly Notes」的 Vault，大家可以下載後用 obsidian 打開，並對照自己的 Vault 設定，看看是哪裡需要做調整，還是不行的話可以再留言詢問。

▼ 匯入方法：解壓縮後，並打開 Obsidian ，選擇「File」->「Open Vault」->「Open Folder as Vault」，選擇解壓縮的資料夾，就能讀取這一份 Vault 囉。

▶▶ [下載我的 Vault 資料夾](https://muki.tw/file/obsidian_mukispace.zip)

## 美化你的 Tasks 圖示

我覺得預設的 Tasks 圖示其實有點 ugly ... XD，所以我有再裝一個套件做美化，如果你喜歡我在範例圖上的這些黑白 icon，可以使用 **[obsidian-tasks-custom-icons](https://github.com/replete/obsidian-tasks-custom-icons)**

[](https://github.com/replete/obsidian-tasks-custom-icons "GitHub - replete/obsidian-tasks-custom-icons: Replace emojis used in Obsidian Tasks with monotone SVGs \(obsidian css snippet generator\)")

GitHub - replete/obsidian-tasks-custom-icons: Replace emojis used in Obsidian Tasks with monotone SVGs (obsidian css snippet generator)

Replace emojis used in Obsidian Tasks with monotone SVGs (obsidian css snippet generator) - replete/obsidian-tasks-custom-icons

他的使用方法很簡單，看到想要用的 icon 圖案後，找到對應的 CSS snippet 後，複製到你的 css 檔案即可，此外也能自己客製化想要的 icon，可以在他的 Read me 文件看到相關介紹唷。

## 結語

這邊因為用了兩個 Plugins，所以在寫作上會跳來跳去的，可能會造成大家的混亂。

但原則上，就是利用 Tasks 管理你的待辦清單，再用 Periodic Notes 搭配 Template 將待辦事項顯示出來，掌握這個流程與原則，應該就不會搞混了。

希望這個 template 對大家有所幫助，也祝大家都能設計出自己心中理想的 Obsidian template 唷！如果有任何問題，也歡迎留言詢問，假設對 template 的設計不太在行，也歡迎留言給我，大家一起想辦法集思廣益 XD。

muki@journal ~/數位筆記生活 $
