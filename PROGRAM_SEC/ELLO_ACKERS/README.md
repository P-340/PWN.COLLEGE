1. Vì sao byte 0x48 ('H') hay xuất hiện?

Trên x86-64, mặc định các lệnh thao tác với thanh ghi 32-bit (eax, edi, esp...). Muốn dùng thanh ghi 64-bit (rax, rdi, rsp...) hoặc một số kiểu toán hạng đặc biệt (như mov qword ptr, sub rsp, imm32...), CPU cần một prefix REX.W = 0x48 đứng trước opcode để báo "operand size = 64-bit".

→ Quy tắc vàng: hễ thấy r đứng đầu tên thanh ghi (rax, rdi, rsp, rsi...) trong code của bạn, khả năng cao sẽ sinh ra byte 0x48.

2. Vì sao phải né rsp/rdi mà vẫn cần giá trị 64-bit đúng?
Stack pointer thật (rsp) là địa chỉ 64-bit nằm ở vùng nhớ cao, không vừa trong 32-bit.
Nếu bạn chỉ lấy esp (32-bit) rồi gán vào edi, bạn làm mất phần cao của địa chỉ → con trỏ sai → segfault khi dùng nó (open/read/write).
Nhưng nếu dùng mov rdi, rsp để lấy đủ 64-bit thì lại dính byte 0x48 (REX.W).
3. Mẹo né REX.W mà vẫn giữ giá trị 64-bit: push/pop
push reg / pop reg ở chế độ 64-bit mặc định đã là 64-bit, không cần REX.W.
Vậy push rsp; pop rdi cho bạn rdi = rsp đầy đủ 64-bit mà không có byte 0x48.
4. Ghi dữ liệu (string) vào stack mà không dùng QWORD
mov qword ptr [rsp], imm64 → luôn cần REX.W (và thực ra immediate 64-bit cũng không encode trực tiếp được kiểu đó).
Thay vào đó, chia nhỏ: mov dword ptr [rsp], imm32 rồi mov word ptr [rsp+4], imm16 — cả hai đều không cần REX.W.
5. Syscall args dùng thanh ghi 32-bit vẫn OK
Khi bạn ghi vào edi, esi, edx, eax (32-bit), CPU tự động zero-extend lên 64-bit tương ứng (rdi, rsi, rdx, rax).
Vì syscall number và nhiều giá trị (fd, flags, mode, length...) đều nhỏ, dùng thanh ghi 32-bit là đủ và an toàn — chỉ riêng con trỏ địa chỉ (pointer) mới cần đủ 64-bit, đó là lý do chỉ pointer mới cần trick push/pop.
Bài học tổng quát

Khi bị cấm 1 byte cụ thể (ở đây là 0x48), chiến thuật chung là:

Hiểu byte đó sinh ra từ đâu (ở đây: REX.W prefix).
Tìm instruction thay thế có cùng hiệu quả nhưng không cần prefix đó (push/pop thay vì mov r64, r64; chia DWORD+WORD thay vì QWORD).
Luôn kiểm tra bảng disasm chương trình in ra để xác nhận bytes thực tế, không chỉ tin vào mnemonic.
