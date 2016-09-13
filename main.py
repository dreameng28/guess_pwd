import sys
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


# 邮件接收函数
def accept_mail():
    try:
        # 你的帐号
        user = 'dreameng28@163.com'
        mailbox = poplib.POP3_SSL('pop.163.com', '995')
        mailbox.user(user)
        mailbox.pass_('5havedreams')
        # 邮件总数
        mails = mailbox.list()[1]
        index = len(mails)
        msgs = []
        # 遍历收件箱
        while index > 0:
            lines = mailbox.retr(index)[1]
            msg_cont = b'\r\n'.join(lines).decode('utf8')
            # print(msg_cont)
            msg = Parser().parsestr(msg_cont)
            msgs.append(msg)
            print_info(msg)
            print(str(index) * 10)
            index -= 1
        mailbox.quit()
        return msgs
    except Exception as e:
        print('Login failed: ', e)
        sys.exit(1)


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))

    if msg.is_multipart():
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s-----------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText:\n %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))

# 运行当前文件时，执行sendmail和accpet_mail函数
if __name__ == "__main__":
    m_msgs = accept_mail()
