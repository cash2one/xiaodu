import struct

from ctypes import *

# NSHEAD_MAGICNUM = 0xfb709394

head_size = 36

class NsHead(Structure):
    _fields_ = [
        ('id', c_uint16),
        ('version', c_uint16),
        ('log_id', c_uint32),
        ('provider', c_char * 16),
        ('magic_num', c_uint32),
        ('reserved', c_uint32),
        ('body_len', c_uint32),
        ]
    _struct_ = struct.Struct('HHI16sIII')
    head_size = 0
    
    def __init__(self):
        self.id = 0
        self.version = 2
        self.log_id = 0
        self.provider = ''
        self.magic_num = 0xfb709394
        self.reserved = 0
        self.body_len = 0
        self.head_size = self._struct_.size

    def pack(self):
        return self._struct_.pack(self.id, self.version, self.log_id, self.provider, self.magic_num,
                           self.reserved, self.body_len)
    to_str = pack

    def unpack(self, binary):
        self.id, self.version, self.log_id, self.provider, self.magic_num, self.reserved, self.body_len \
            = self._struct_.unpack(binary)

    @classmethod
    def from_str(cls, string):
        if len(string) != sizeof(cls):
            return False
        buf = create_string_buffer(string)
        return cls.from_buffer(buf)

    def __str__(self):
        return "<NsHead id:%d logid:%d provider:%s magic:0x%X bodylen:%s>" % (
            self.id, self.log_id, self.provider, self.magic_num, self.body_len)

def test():
    str1 = "hello world"
    ns = NsHead()
    ns.body_len = len(str1)
    binary = ns.pack()
    print len(binary)
    print ns.head_size
    ns2 = NsHead()
    ns2.unpack(binary)
    print ns2



if __name__ == "__main__":
    test()
