---
source: "https://www.cnblogs.com/shihaiming/p/6282226.html"
title: "SpringMVC整合fastdfs-client-java实现web文件上传下载 - 这个名字想了很久~ - 博客园"
fetched_at: "2026-10-05 15:32:38"
---

原文：http://blog.csdn.net/wlwlwlwl015/article/details/52682153

本篇blog主要记录一下SpringMVC整合FastDFS的[Java](http://lib.csdn.net/base/17 "Java EE知识库")客户端实现web中的文件上传与下载。

![](https://images2015.cnblogs.com/blog/1000885/201701/1000885-20170113115555056-91511933.png)

# 下载编译

在余大的GitHub上可以下载到fastdfs-client-java的源代码：

https://github.com/happyfish100/fastdfs-client-java

![](https://images2015.cnblogs.com/blog/1000885/201701/1000885-20170113115340963-1030092118.png)

如上图，这个版本是通过JDK1.5编译的，根据需求可以通过源码重新编译jar包，我这里将原项目的maven编译插件的版本改为JDK 1.8之后重新进行了编译，编译安装成功后可以在我们本地的maven仓库看到fastdfs-client-java的jar包：

![](https://images2015.cnblogs.com/blog/1000885/201701/1000885-20170113115624103-755598193.png)

最后在我们项目的pom中添加fastdfs-client-java的坐标信息就OK了：


    <!-- fastdfs-client -->
    <dependency>
        <groupId>org.csource</groupId>
        <artifactId>fastdfs-client-java</artifactId>
        <version>1.25</version>
    </dependency>

# 文件上传

首先来实现文件上传，fastdfs-client-java的上传是通过传入一个byte[ ]来完成的，简单看一下源码：


    public String[] upload_file(byte[] file_buff, String file_ext_name,
               NameValuePair[] meta_list) throws IOException, MyException{
        final String group_name = null;
        return this.upload_file(group_name, file_buff, 0, file_buff.length, file_ext_name, meta_list);
    }

如上所示，暂且不再深入研究原理，此处我们知道需要一个byte[ ]类型的参数就可以了，而SpringMVC的文件上传用到的MultipartFile对象可以直接通过getBytes方法得到文件的byte[ ]，也就是CommonsMultipartFile类中的getBytes()，源码如下：


    @Override
    public byte[] getBytes() {
        if (!isAvailable()) {
            throw new IllegalStateException("File has been moved - cannot be read again");
        }
        byte[] bytes = this.fileItem.get();
        return (bytes != null ? bytes : new byte[0]);
    }

那么接下来我们就知道如何上传了，当然首先需要做一些简单的封装，这里把文件上传的相关属性封装在了一个接口中，需要用到文件上传的相关实体或者工具类直接实现这个接口即可：


    public interface FileManagerConfig extends Serializable {

        public static final String FILE_DEFAULT_AUTHOR = "WangLiang";

        public static final String PROTOCOL = "http://";

        public static final String SEPARATOR = "/";

        public static final String TRACKER_NGNIX_ADDR = "192.168.0.68";

        public static final String TRACKER_NGNIX_PORT = "";

        public static final String CLIENT_CONFIG_FILE = "fdfs_client.conf";
    }

接下来定义FastDFS文件的实体类：


    package com.wl.bean;


    /**
     * <strong>类概要： FastDFS文件实体</strong>
     * <strong>创建时间： 2016-9-27 下午10:29:25</strong>
     *
     * @Project springmvc-main(com.wl.bean)
     * @author Wang Liang
     * @version 1.0.0
     */
    public class FastDFSFile implements FileManagerConfig {

        private static final long serialVersionUID = 1L;

        private byte[] content;
        private String name;
        private String ext;
        private String length;
        private String author = FILE_DEFAULT_AUTHOR;

        public FastDFSFile(byte[] content, String ext) {
            this.content = content;
            this.ext = ext;
        }

        public FastDFSFile(byte[] content, String name, String ext) {
            this.content = content;
            this.name = name;
            this.ext = ext;
        }

        public FastDFSFile(byte[] content, String name, String ext, String length,
                String author) {
            this.content = content;
            this.name = name;
            this.ext = ext;
            this.length = length;
            this.author = author;
        }

        public byte[] getContent() {
            return content;
        }

        public void setContent(byte[] content) {
            this.content = content;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        public String getExt() {
            return ext;
        }

        public void setExt(String ext) {
            this.ext = ext;
        }

        public String getLength() {
            return length;
        }

        public void setLength(String length) {
            this.length = length;
        }

        public String getAuthor() {
            return author;
        }

        public void setAuthor(String author) {
            this.author = author;
        }

    }

如上所示，包括上传所必须的file_buff和file_ext_name以及在meta_list中存放的几个文件描述属性。接下来看一下核心工具类FileManager：


    import java.io.File;
    import java.io.IOException;

    import org.csource.common.NameValuePair;
    import org.csource.fastdfs.ClientGlobal;
    import org.csource.fastdfs.StorageClient;
    import org.csource.fastdfs.StorageServer;
    import org.csource.fastdfs.TrackerClient;
    import org.csource.fastdfs.TrackerServer;
    import org.springframework.http.HttpHeaders;
    import org.springframework.http.HttpStatus;
    import org.springframework.http.MediaType;
    import org.springframework.http.ResponseEntity;

    /**
     * <strong>类概要： FastDFS Java客户端工具类</strong>
     * <strong>创建时间： 2016-9-26 上午10:26:48</strong>
     *
     * @Project springmvc-main(com.wl.bean)
     * @author Wang Liang
     * @version 1.0.0
     */
    public class FileManager implements FileManagerConfig {

        private static final long serialVersionUID = 1L;
        private static TrackerClient trackerClient;
        private static TrackerServer trackerServer;
        private static StorageServer storageServer;
        private static StorageClient storageClient;

        static {
            try {
                String classPath = new File(FileManager.class.getResource("/").getFile()).getCanonicalPath();

                String fdfsClientConfigFilePath = classPath + File.separator + CLIENT_CONFIG_FILE;
                ClientGlobal.init(fdfsClientConfigFilePath);

                trackerClient = new TrackerClient();
                trackerServer = trackerClient.getConnection();

                storageClient = new StorageClient(trackerServer, storageServer);

            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        /**
         * <strong>方法概要： 文件上传</strong>
         * <strong>创建时间： 2016-9-26 上午10:26:11</strong>
         *
         * @param FastDFSFile
         *            file
         * @return fileAbsolutePath
         * @author Wang Liang
         */
        public static String upload(FastDFSFile file,NameValuePair[] valuePairs) {
            String[] uploadResults = null;
            try {
                uploadResults = storageClient.upload_file(file.getContent(),file.getExt(), valuePairs);
            } catch (Exception e) {
                e.printStackTrace();
            }
            String groupName = uploadResults[0];
            String remoteFileName = uploadResults[1];

            String fileAbsolutePath = PROTOCOL
                    + TRACKER_NGNIX_ADDR
                    //+ trackerServer.getInetSocketAddress().getHostName()
                    //+ SEPARATOR + TRACKER_NGNIX_PORT
                    + SEPARATOR + groupName
                    + SEPARATOR + remoteFileName;
            return fileAbsolutePath;
        }
    }

如上所示，在类初始化时加载fdfs_client.conf配置文件并构造tracker server和storage server，文件上传是通过`storageClient.upload_file`方法来实现的，而返回的uploadResults字符串数组正是文件名，固定两个元素，uploadResults[0]是组名（group），而uploadResults[1]就是组名后面的文件全名了，最后我们的方法中有做了部分拼接使得FileManager.upload直接可以返回完成的文件路径，下面就是我们调用上传方法的controller中的方法了：


    @RequestMapping(value = "/add", method = RequestMethod.POST)
    public String add(@Validated User user, BindingResult br,MultipartFile attach, HttpServletRequest request)
            throws IOException, MyException {
        if (br.hasErrors()) {
            return "user/add";
        }
        // 获取文件后缀名
        String ext = attach.getOriginalFilename().substring(attach.getOriginalFilename().lastIndexOf(".")+1);
        FastDFSFile file = new FastDFSFile(attach.getBytes(),ext);
        NameValuePair[] meta_list = new NameValuePair[4];
        meta_list[0] = new NameValuePair("fileName", attach.getOriginalFilename());
        meta_list[1] = new NameValuePair("fileLength", String.valueOf(attach.getSize()));
        meta_list[2] = new NameValuePair("fileExt", ext);
        meta_list[3] = new NameValuePair("fileAuthor", "WangLiang");
        String filePath = FileManager.upload(file,meta_list);
        user.setFilePath(filePath);
        users.put(user.getUsername(), user);
        return "redirect:/user/users";
    }

如上所示，首先通过字符串截取得到上传文件的后缀名，然后通过文件后缀和文件的byte[ ]构造FastDFSFile对象，接着构造meta_list的NameValuePair[] 数组，这里主要是对文件的可选性描述信息，最后通过FileManager.upload即可完成上传并返回该文件的绝对访问路径，可以根据需要存入DB或文件等等，没有报异常就说明文件上传成功，接下来看看文件下载。

# 文件下载

fastdfs-client-java提供的文件下载的api需要两个参数，分别是group_name（组名）和remote_filename（文件名），源码如下：


    /**
    * download file from storage server
    * @param group_name the group name of storage server
    *   @param remote_filename filename on storage server
    * @return file content/buff, return null if fail
    */
    public byte[] download_file(String group_name, String remote_filename) throws IOException, MyException
    {
        final long file_offset = 0;
        final long download_bytes = 0;

        return this.download_file(group_name, remote_filename, file_offset, download_bytes);
    }

所以我们仅需在这里得到group_name和remote_filename即可，因为之前我们在文件上传时候已经保存了图片的绝对路径（`user.setFilePath(filePath)`），所以在此处仅需要获取到绝对路径并进行字符串的拆分截取即可，接下来先看一下封装在FileManager中的下载方法：


    /**
     * <strong>方法概要： 文件下载</strong>
     * <strong>创建时间： 2016-9-26 上午10:28:21</strong>
     *
     * @param String
     *            groupName
     * @param String
     *            remoteFileName
     * @return returned value comment here
     * @author Wang Liang
     */
    public static ResponseEntity<byte[]> download(String groupName,
            String remoteFileName,String specFileName) {
        byte[] content = null;
        HttpHeaders headers = new HttpHeaders();
        try {
            content = storageClient.download_file(groupName, remoteFileName);
            headers.setContentDispositionFormData("attachment",  new String(specFileName.getBytes("UTF-8"),"iso-8859-1"));
            headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        return new ResponseEntity<byte[]>(content, headers, HttpStatus.CREATED);
    }

如上所示，17行调用fastdfs-client-java提供的下载方法，下载成功后返回的是一个byte[ ]，刚好结合SpringMVC官方推荐的构造HttpEntity的方式即可实现文件下载，这个download方法我多指定了一个参数**specFileName** 目的是保证给客户端看到的下载后的文件名是通过程序来自定义的，而不是fastdfs服务器上的那一长串默认字符串，**18行指定了utf-8编码使得我们自定义的文件名支持中文，这一点很重要，否则将无法正确下载我们重命名后的包含中文的文件** 。最后在看一下controller中的下载方法：


    @RequestMapping(value = "/{username}/download", method = RequestMethod.GET)
    public ResponseEntity<byte[]> download(@PathVariable String username, Model model,HttpServletResponse response) throws IOException, MyException {
        User u = users.get(username);
        String filePath = u.getFilePath();
        String substr = filePath.substring(filePath.indexOf("group"));
        String group = substr.split("/")[0];
        String remoteFileName = substr.substring(substr.indexOf("/")+1);
        String specFileName = username + substr.substring(substr.indexOf("."));
        return FileManager.download(group, remoteFileName,specFileName);
    }

同我们之前的想法一样，截取文件的绝对路径分别得到**group_name** 以及**file_name** ，而传入的specFileName我们这里自定义为**用户名（username）** +截取后的**文件后缀名** ，看一下效果：
![这里写图片描述](https://img-blog.csdn.net/20161004170908567)
![这里写图片描述](https://img-blog.csdn.net/20161004170919426)

如上图，点击【下载附件】，即可正确下载以及重命名文件，至此SpringMVC结合fastdfs的文件上传下载就已全部结束了。
