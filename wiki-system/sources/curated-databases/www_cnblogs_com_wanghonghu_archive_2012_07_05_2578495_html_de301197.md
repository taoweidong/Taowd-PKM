---
source: "http://www.cnblogs.com/wanghonghu/archive/2012/07/05/2578495.html"
title: "C#写入和读出文本文件 - 蒹葭白露 - 博客园"
fetched_at: "2026-10-05 15:29:41"
---

* **写入文本文件**



        class WriteTextFile
        {
            static void Main()
            {
                //如果文件不存在，则创建；存在则覆盖
                //该方法写入字符数组换行显示
                string[] lines = { "first line", "second line", "third line","第四行" };
                System.IO.File.WriteAllLines(@"C:\testDir\test.txt", lines, Encoding.UTF8);

                //如果文件不存在，则创建；存在则覆盖
                string strTest = "该例子测试一个字符串写入文本文件。";
                System.IO.File.WriteAllText(@"C:\testDir\test1.txt", strTest, Encoding.UTF8);

                //在将文本写入文件前，处理文本行
                //StreamWriter一个参数默认覆盖
                //StreamWriter第二个参数为false覆盖现有文件，为true则把文本追加到文件末尾
                using (System.IO.StreamWriter file = new System.IO.StreamWriter(@"C:\testDir\test2.txt",true))
                {
                    foreach (string line in lines)
                    {
                        if (!line.Contains("second"))
                        {
                            file.Write(line);//直接追加文件末尾，不换行
                            file.WriteLine(line);// 直接追加文件末尾，换行
                        }
                    }
                }
            }
        }

  * **读取文本文件**



        class ReadTextFile
        {
            static void Main()
            {
                //直接读取出字符串
                string text = System.IO.File.ReadAllText(@"C:\testDir\test1.txt");
                Console.WriteLine(text);

                //按行读取为字符串数组
                string[] lines = System.IO.File.ReadAllLines(@"C:\testDir\test.txt");
                foreach (string line in lines)
                {
                    Console.WriteLine(line);
                }

                //从头到尾以流的方式读出文本文件
                //该方法会一行一行读出文本
                using (System.IO.StreamReader sr = new System.IO.StreamReader(@"C:\testDir\test.txt"))
                {
                    string str;
                    while ((str = sr.ReadLine()) != null)
                    {
                        Console.WriteLine(str);
                    }
                }
                Console.Read();
            }
        }
