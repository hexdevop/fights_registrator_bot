select-tournament = <i><b>🏆 Turnirlardan birini tanlang</></>

tournament-info =
    <i><b>{$name}</>

    📅 Tadbir sanasi - {$date}
    🏢 Tashkilotchi - {$organizer}
    👥 Yosh - {$age}</>

select-discipline = <i><b>🎯 Turnir intizomini tanlang</></>

select-region = <i><b>🌍 Mintaqangizni tanlang</></>

get-initials = <i><b>👤 Lotin tilida to'liq ismingizni (familiyangizni, ismingizni, otasining ismini) kiriting</></>

get-coach-initials = <i><b>👨‍🏫 Treneringizning to'liq ismini (familiyasi, ismi, otasining ismi) lotin tilida kiriting</></>

get-age =
    <i><b>📅 Iltimos, tug'ilgan kuningizni yil-oy-kun formatida kiriting
    Misol: 1999-10-23</></>

select-gender = <i><b>👫 Jinsingizni tanlang</></>

select-weight = <i><b>⚖️ O'zingizning vazn toifangizni tanlang</></>

confirm-registration =
    <i><b>Ro'yxatdan o'tishni yakunlashdan oldin kiritilgan ma'lumotlarni tekshiring.:</>

    🏆 Turnir: {$tournament}
    🎯 Intizom: {$discipline}
    🌍 Mintaqa: {$region}
    👤 To'liq ism: {$initials}
    👨‍🏫 Trener: {$coach_initials}
    📅 Tug'ilgan kuni: {$date}
    👫 Jins: {$gender ->
[1] 🤵‍♂️ Erkak
*[0] 🧍‍♀️ Ayol
}
    ⚖️ Og'irlik toifasi: {$weight}</>

you-was-registered = <i>Roʻyxatdan oʻtish muvaffaqiyatli yakunlandi! ✅</>

# ERRORS

tournament-stopped = ❌ Ushbu turnir uchun ro'yxatga olish yopiq yoki yopiq.

incorrect-age =
    <i><b>❌ Noto'g'ri sana</>
    Iltimos, tug'ilgan kuningizni yil-oy-kun formatida kiriting
    Misol: 1999-10-23</>

age-limit =
    <i><b>❌ Sizning yoshingiz turnir talablariga javob bermaydi</>
    Turnir {$min_age} dan {$max_age} yoshgacha bo‘lganlar uchun mo‘ljallangan
    Roʻyxatdan oʻtish bekor qilindi</>

