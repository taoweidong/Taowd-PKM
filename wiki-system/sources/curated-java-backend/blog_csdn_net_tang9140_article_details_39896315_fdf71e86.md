---
source: "https://blog.csdn.net/tang9140/article/details/39896315"
title: "spring_jdbc数据库配置项中用户名及密码密文处理类(防黑客入侵用)_如何保障jdbc里面得用户名和密码不泄露-CSDN博客"
fetched_at: "2026-10-05 15:32:28"
---

### 原始配置

spring结合mysql，一般是单独出配置文件jdbc.properties,

配置如下


    driverClassName=com.mysql.jdbc.Driver
    db.mysql.url=jdbc:mysql://127.0.0.1:3306/tq?autoReconnect=true&useUnicode=true&characterEncoding=utf8
    db.mysql.username=test
    db.mysql.password=123456

配置spring-jdbc.xml，使其加载该配置项。示例如下：


    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
    	xmlns:aop="http://www.springframework.org/schema/aop" xmlns:context="http://www.springframework.org/schema/context"
    	xmlns:mvc="http://www.springframework.org/schema/mvc" xmlns:tx="http://www.springframework.org/schema/tx"
    	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    	xsi:schemaLocation="http://www.springframework.org/schema/aop
    		http://www.springframework.org/schema/aop/spring-aop-3.0.xsd
    		http://www.springframework.org/schema/beans
    		http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
    		http://www.springframework.org/schema/context
    		http://www.springframework.org/schema/context/spring-context-3.0.xsd
    		http://www.springframework.org/schema/mvc
    		http://www.springframework.org/schema/mvc/spring-mvc-3.0.xsd
    		http://www.springframework.org/schema/tx
    		http://www.springframework.org/schema/tx/spring-tx-3.0.xsd"
    	default-autowire="byName">

    	<context:annotation-config />
    	<!-- 扫描组件，完成自动装配 -->
    	<context:component-scan base-package="com.tq.app.epg.dao" />

    	<bean id="propertyConfigurer"
    		class="org.springframework.beans.factory.config.PropertyPlaceholderConfigurer">

    			<list>
    				<value>classpath:jdbc.properties</value>
    			</list>

    	</bean>
    	<bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource"
    		destroy-method="close" lazy-init="true" depends-on="propertyConfigurer">













    	</bean>

    	<bean id="jdbcTemplate" class="org.springframework.jdbc.core.JdbcTemplate">

        	</bean>

    </beans>



按上面进行配置，由于数据库连接、账号、密码是明文，存在泄露风险。可以在配置文件中存密文，在spring读取该配置文件时，进行解密。

### 改进配置


    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
    	xmlns:aop="http://www.springframework.org/schema/aop" xmlns:context="http://www.springframework.org/schema/context"
    	xmlns:mvc="http://www.springframework.org/schema/mvc" xmlns:tx="http://www.springframework.org/schema/tx"
    	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    	xsi:schemaLocation="http://www.springframework.org/schema/aop
    		http://www.springframework.org/schema/aop/spring-aop-3.0.xsd
    		http://www.springframework.org/schema/beans
    		http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
    		http://www.springframework.org/schema/context
    		http://www.springframework.org/schema/context/spring-context-3.0.xsd
    		http://www.springframework.org/schema/mvc
    		http://www.springframework.org/schema/mvc/spring-mvc-3.0.xsd
    		http://www.springframework.org/schema/tx
    		http://www.springframework.org/schema/tx/spring-tx-3.0.xsd"
    	default-autowire="byName">

    	<context:annotation-config />
    	<!-- 扫描组件，完成自动装配 -->
    	<context:component-scan base-package="com.tq.app.epg.dao" />

    	<bean id="propertyConfigurer"
    		class="com.tq.app.epg.utils.config.GvtvPropertyPlaceholderConfigurer">

    			<list>
    				<value>classpath:jdbc.properties</value>
    			</list>

    	</bean>
    	<bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource"
    		destroy-method="close" lazy-init="true" depends-on="propertyConfigurer">













    	</bean>

    	<bean id="jdbcTemplate" class="org.springframework.jdbc.core.JdbcTemplate">

        	</bean>
    </beans>

注意上面类GvtvPropertyPlaceholderConfigurer，该类的实现如下：


    package com.tq.app.epg.utils.config;

    import java.util.Enumeration;
    import java.util.Properties;

    import org.springframework.beans.BeansException;
    import org.springframework.beans.factory.config.ConfigurableListableBeanFactory;
    import org.springframework.beans.factory.config.PropertyPlaceholderConfigurer;

    public class GvtvPropertyPlaceholderConfigurer extends PropertyPlaceholderConfigurer {
        @Override
        protected void processProperties(ConfigurableListableBeanFactory beanFactoryToProcess, Properties props) throws BeansException {

            AESHelper aesHelper = new AESHelper();
            Enumeration<?> keys = props.propertyNames();
            while (keys.hasMoreElements()) {
                String key = (String)keys.nextElement();
                String value = props.getProperty(key);
                if (key.endsWith(".encryption") && null != value) {
                    props.remove(key);
                    key = key.substring(0, key.length() - 11);
                    value = aesHelper.decrypt(value.trim());
                    props.setProperty(key, value);
                }
                System.setProperty(key, value);
            }

            super.processProperties(beanFactoryToProcess, props);
        }
    }

相应的jdbc.properties变为


    driverClassName=com.mysql.jdbc.Driver
    db.mysql.url.encryption=XXXXXXXXXXXXXXXXXXXXXXX
    db.mysql.username.encryption=D12450E55E370A310C1AAAB5189BB42A
    db.mysql.password.encryption=ADC6327D7DB1D55623B70B48614A331B




另附AESHelper类：


    package com.tq.app.epg.utils.config;

    import java.io.InputStream;
    import java.io.OutputStream;
    import java.security.MessageDigest;
    import java.security.spec.AlgorithmParameterSpec;

    import javax.crypto.Cipher;
    import javax.crypto.CipherInputStream;
    import javax.crypto.CipherOutputStream;
    import javax.crypto.SecretKey;
    import javax.crypto.spec.IvParameterSpec;
    import javax.crypto.spec.SecretKeySpec;

    /**
     * <一句话功能简述>
     */
    public class AESHelper {
        Cipher ecipher;

        Cipher dcipher;

        /**
         * Input a string that will be md5 hashed to create the key.
         *
         * @return void, cipher initialized
         */
        public AESHelper() {
            try {
                SecretKeySpec skey = new SecretKeySpec("9f265d42ab3c66d8f50a3a2e793a30c2".getBytes(), "AES");
                this.setupCrypto(skey);
            }
            catch (Exception e) {
                e.printStackTrace();
            }
        }

        public AESHelper(String key) {
            SecretKeySpec skey = new SecretKeySpec(getMD5(key), "AES");
            this.setupCrypto(skey);
        }

        private void setupCrypto(SecretKey key) {
            // Create an 8-byte initialization vector
            byte[] iv = new byte[]
            {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};

            AlgorithmParameterSpec paramSpec = new IvParameterSpec(iv);
            try {
                ecipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
                dcipher = Cipher.getInstance("AES/CBC/PKCS5Padding");

                // CBC requires an initialization vector
                ecipher.init(Cipher.ENCRYPT_MODE, key, paramSpec);
                dcipher.init(Cipher.DECRYPT_MODE, key, paramSpec);
            }
            catch (Exception e) {
                e.printStackTrace();
            }
        }

        // Buffer used to transport the bytes from one stream to another
        // byte[] buf = new byte[1024];

        public void encrypt(InputStream in, OutputStream out) {
            byte[] buf = new byte[1024];
            try {
                // Bytes written to out will be encrypted
                out = new CipherOutputStream(out, ecipher);

                // Read in the cleartext bytes and write to out to encrypt
                int numRead = 0;
                while ((numRead = in.read(buf)) >= 0) {
                    out.write(buf, 0, numRead);
                }
                out.close();
            }
            catch (java.io.IOException e) {
                e.printStackTrace();
            }
        }

        /**
         * Input is a string to encrypt.
         *
         * @return a Hex string of the byte array
         */
        public String encrypt(String plaintext) {
            try {
                byte[] ciphertext = ecipher.doFinal(plaintext.getBytes("UTF-8"));
                return byteToHex(ciphertext);
            }
            catch (Exception e) {
                e.printStackTrace();
                return null;
            }

        }

        public void decrypt(InputStream in, OutputStream out) {
            try {
                byte[] buf = new byte[1024];
                // Bytes read from in will be decrypted
                in = new CipherInputStream(in, dcipher);

                // Read in the decrypted bytes and write the cleartext to out
                int numRead = 0;
                while ((numRead = in.read(buf)) >= 0) {
                    out.write(buf, 0, numRead);
                }
                out.close();
            }
            catch (java.io.IOException e) {
                e.printStackTrace();
            }
        }

        /**
         * Input encrypted String represented in HEX
         *
         * @return a string decrypted in plain text
         */
        public String decrypt(String hexCipherText) {
            try {
                String plaintext = new String(dcipher.doFinal(hexToByte(hexCipherText)), "UTF-8");
                return plaintext;
            }
            catch (Exception e) {
                e.printStackTrace();
                return null;
            }
        }

        public String decrypt(byte[] ciphertext) {
            try {
                String plaintext = new String(dcipher.doFinal(ciphertext), "UTF-8");
                return plaintext;
            }
            catch (Exception e) {
                e.printStackTrace();
                return null;
            }
        }

        private static byte[] getMD5(String input) {
            try {
                byte[] bytesOfMessage = input.getBytes("UTF-8");
                MessageDigest md = MessageDigest.getInstance("MD5");
                return md.digest(bytesOfMessage);
            }
            catch (Exception e) {
                return null;
            }
        }

        static final String HEXES = "0123456789ABCDEF";

        public static String byteToHex(byte[] raw) {
            if (raw == null) {
                return null;
            }
            final StringBuilder hex = new StringBuilder(2 * raw.length);
            for (final byte b : raw) {
                hex.append(HEXES.charAt((b & 0xF0) >> 4)).append(HEXES.charAt((b & 0x0F)));
            }
            return hex.toString();
        }

        public static byte[] hexToByte(String hexString) {
            int len = hexString.length();
            byte[] ba = new byte[len / 2];
            for (int i = 0; i < len; i += 2) {
                ba[i / 2] =
                    (byte)((Character.digit(hexString.charAt(i), 16) << 4) + Character.digit(hexString.charAt(i + 1), 16));
            }
            return ba;
        }

    }
