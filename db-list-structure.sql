CREATE TABLE `t_send_mail_attachments`
(
    `id`                     int(11)      NOT NULL AUTO_INCREMENT COMMENT '附件ID',
    `t_send_mail_history_id` int(11)      NOT NULL COMMENT '关联邮件发送历史记录id',
    `filename_md5`           varchar(200) NOT NULL COMMENT '附件 MD5 值',
    `original_filename`      varchar(200) NOT NULL COMMENT '附件的原始文件名',
    `create_time`            datetime DEFAULT current_timestamp() COMMENT '创建时间',
    `update_time`            datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 61
  DEFAULT CHARSET = utf8mb3
  COLLATE = utf8mb3_uca1400_ai_ci COMMENT ='附件表，存储每个附件的 MD5 和原始文件名';
CREATE TABLE `t_send_mail_history`
(
    `id`                int(11)      NOT NULL AUTO_INCREMENT COMMENT '邮件任务ID',
    `email_recipients`  longtext     NOT NULL,
    `email_title`       varchar(200) NOT NULL COMMENT '邮件标题',
    `email_text`        longtext     NOT NULL,
    `email_send_status` longtext     NOT NULL,
    `client_ip_address` varchar(100) NOT NULL COMMENT '客户端 IP 地址',
    `create_time`       datetime     NOT NULL DEFAULT current_timestamp() COMMENT '创建时间，默认当前时间',
    `update_time`       datetime     NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '更新时间，随更新自 动更新',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 52
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_uca1400_ai_ci COMMENT ='邮件发送历史记录表';