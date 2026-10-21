import { useMemo, useState } from 'react'
import {
  Activity, ArrowDownLeft, ArrowLeft, ArrowUpLeft, Bell, CalendarDays, Check,
  ChevronDown, ChevronLeft, Clock3, Coins, Download, GraduationCap, HandHeart,
  LayoutDashboard, Menu, MessageSquareText, Plus, Search, Settings2, ShieldCheck,
  Sparkles, Star, UsersRound, Wallet, X, UserRoundPlus,
} from 'lucide-react'

type View = 'overview' | 'committees' | 'events' | 'volunteers' | 'evaluations' | 'finance'
type Committee = { name: string; icon: string; color: string; count: number; note: string }

const committees: Committee[] = [
  { name: 'لجنة الأنشطة', icon: '✳', color: 'amber', count: 11, note: 'الفعاليات واللقاءات الطلابية' },
  { name: 'لجنة التقنية', icon: '⌘', color: 'blue', count: 14, note: 'المنصات والدعم التقني' },
  { name: 'لجنة الإعلام', icon: '◉', color: 'pink', count: 8, note: 'المحتوى والتصميم والتغطية' },
  { name: 'لجنة العلاقات العامة', icon: '↗', color: 'violet', count: 7, note: 'الشراكات والتواصل المؤسسي' },
  { name: 'أنشطة الذكاء الاصطناعي', icon: '✧', color: 'mint', count: 12, note: 'ورش وفعاليات الذكاء الاصطناعي' },
]

const baseVolunteers = [
  { name: 'سارة منصور', initials: 'سم', committee: 'لجنة الإعلام', status: 'نشطة', events: 8, hours: 22, note: 'تغطية مميزة لفعالية الأسبوع الماضي، والتزام واضح بتأكيد فترات الحضور.' },
  { name: 'أحمد خالد', initials: 'أخ', committee: 'لجنة التقنية', status: 'نشط', events: 6, hours: 18, note: 'ساهم في تجهيز القاعة التقنية وتعاون مع فريق التسجيل.' },
  { name: 'ليان عودة', initials: 'لع', committee: 'لجنة الأنشطة', status: 'نشطة', events: 5, hours: 16, note: 'مبادرة في تنظيم الاستقبال، ويُفضّل تأكيد التوفر بوقت أبكر.' },
  { name: 'محمد ناصر', initials: 'من', committee: 'أنشطة الذكاء الاصطناعي', status: 'نشط', events: 4, hours: 13, note: 'مشاركة فعالة في ورشة تعلم الآلة.' },
]

const nav: { id: View; label: string; icon: typeof LayoutDashboard }[] = [
  { id: 'overview', label: 'الرئيسية', icon: LayoutDashboard },
  { id: 'committees', label: 'اللجان', icon: UsersRound },
  { id: 'events', label: 'الفعاليات والتوفر', icon: CalendarDays },
  { id: 'volunteers', label: 'المتطوعون', icon: HandHeart },
  { id: 'evaluations', label: 'التقييمات والملاحظات', icon: Star },
  { id: 'finance', label: 'الصندوق', icon: Wallet },
]

const shifts = [
  { id: 1, title: 'التجهيز', time: '٨:٠٠ – ٩:٣٠ ص', need: 4, assigned: 3, tint: 'mint', people: ['سم', 'لع', 'أخ'] },
  { id: 2, title: 'الاستقبال', time: '٩:٣٠ ص – ١٢:٠٠ م', need: 3, assigned: 2, tint: 'blue', people: ['من', 'سم'] },
  { id: 3, title: 'تنظيم القاعة', time: '١٢:٠٠ – ٢:٠٠ م', need: 3, assigned: 3, tint: 'violet', people: ['أخ', 'لع', 'من'] },
  { id: 4, title: 'الإغلاق', time: '٢:٠٠ – ٤:٠٠ م', need: 4, assigned: 1, tint: 'pink', people: ['سم'] },
]

function Brand() {
  return <div className="brand-lockup"><div className="brand-mark"><span>ن</span><i /></div><div><strong>NAI</strong><small>جمعية ناي للذكاء الاصطناعي</small></div></div>
}

function Avatar({ initials, tone = 'purple' }: { initials: string; tone?: string }) {
  return <span className={`avatar avatar-${tone}`}>{initials}</span>
}

function App() {
  const [view, setView] = useState<View>('overview')
  const [selected, setSelected] = useState<number[]>([1, 2])
  const [savedAvailability, setSavedAvailability] = useState(false)
  const [activeCommittee, setActiveCommittee] = useState('الكل')
  const [noteText, setNoteText] = useState('')
  const [savedNote, setSavedNote] = useState('')
  const [mobileOpen, setMobileOpen] = useState(false)
  const [toast, setToast] = useState('')
  const [volunteers, setVolunteers] = useState(baseVolunteers)
  const [registerOpen, setRegisterOpen] = useState(false)
  const [registerBusy, setRegisterBusy] = useState(false)
  const [registerError, setRegisterError] = useState('')
  const [registerRole, setRegisterRole] = useState('member')
  const [authMode, setAuthMode] = useState<'login' | 'register'>('register')

  const filteredVolunteers = useMemo(() => activeCommittee === 'الكل' ? volunteers : volunteers.filter((person) => person.committee === activeCommittee), [activeCommittee, volunteers])
  const notify = (message: string) => { setToast(message); window.setTimeout(() => setToast(''), 2400) }
  const changeView = (next: View) => { setView(next); setMobileOpen(false) }

  const heading = {
    overview: ['أهلاً سارة،', 'هذه لمحة عن مجتمع ناي اليوم.'],
    committees: ['اللجان', 'مساحات العمل والفرق التطوعية في الجمعية.'],
    events: ['الفعاليات والتوفر', 'نظّم فترات الفعالية واجمع أوقات توفر المتطوعين.'],
    volunteers: ['المتطوعون', 'تابع المشاركة والحضور وملاحظات اللجان.'],
    evaluations: ['التقييمات والملاحظات', 'تغذية راجعة بنّاءة مرتبطة بمشاركة فعلية.'],
    finance: ['الصندوق', 'متابعة شفافة لسجلات المصروفات والإيرادات.'],
  }[view]

  function saveNote() {
    if (!noteText.trim()) { notify('اكتبي الملاحظة قبل الحفظ'); return }
    setSavedNote(noteText.trim())
    setVolunteers((old) => old.map((person, i) => i === 0 ? { ...person, note: noteText.trim() } : person))
    setNoteText('')
    notify('تم حفظ الملاحظة في ملف المتطوع')
  }

  async function submitRegistration(form: HTMLFormElement) {
    setRegisterBusy(true)
    setRegisterError('')
    const formData = new FormData(form)
    const payload = Object.fromEntries(formData.entries())
    try {
      const csrf = await fetch('/api/auth/csrf/', { credentials: 'include' })
      if (!csrf.ok) throw new Error('تعذّر الاتصال بالخادم. شغّل Django ثم حاول مرة ثانية.')
      const { csrfToken } = await csrf.json() as { csrfToken: string }
      const response = await fetch(authMode === 'register' ? '/api/auth/register/' : '/api/auth/session/', {
        method: 'POST', credentials: 'include',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
        body: JSON.stringify(authMode === 'register' ? payload : { ...payload, action: 'login' }),
      })
      const result = await response.json()
      if (!response.ok) throw new Error(result.detail || 'تعذّر إرسال الطلب. تحقق من البيانات.')
      setRegisterOpen(false)
      notify(authMode === 'register' ? 'وصل طلب إنشاء الحساب. الصلاحيات تتفعّل بعد مراجعة الإدارة.' : result.active ? 'تم تسجيل الدخول بنجاح.' : 'الحساب بانتظار اعتماد الإدارة.')
      form.reset()
    } catch (error) {
      setRegisterError(error instanceof Error ? error.message : 'حدث خطأ غير متوقع.')
    } finally {
      setRegisterBusy(false)
    }
  }

  function renderOverview() {
    return <>
      <section className="hero-banner">
        <img src="/campus-banner.webp" alt="حدائق ومباني جامعة النجاح الوطنية بإضاءة بنفسجية" />
        <div className="hero-wash" />
        <div className="hero-copy"><span className="eyebrow"><Sparkles size={14} /> مجتمع طلابي، أثر حقيقي</span><h2>نبني مجتمعاً<br />يصنع <em>المستقبل</em></h2><p>مساحة موحدة لإدارة لجان ناي وفعالياتها، ومساندة كل متطوع ليكون جزءاً من الأثر.</p><button className="button button-primary" onClick={() => changeView('events')}>تنظيم فعالية <ArrowLeft size={16} /></button></div>
        <div className="hero-note"><span className="note-icon"><GraduationCap size={20} /></span><span><b>جامعة النجاح الوطنية</b><small>مجتمع الذكاء الاصطناعي الطلابي</small></span></div>
      </section>
      <section className="stat-grid">
        <StatCard icon={UsersRound} label="المنتسبون" value="320" delta="أعضاء المجتمع" tone="purple" />
        <StatCard icon={HandHeart} label="المتطوعون" value="64" delta="عبر اللجان الخمس" tone="blue" />
        <StatCard icon={CalendarDays} label="فعاليات قادمة" value="08" delta="خلال هذا الفصل" tone="pink" />
        <StatCard icon={ShieldCheck} label="بانتظار المراجعة" value="12" delta="تحتاج متابعة" tone="mint" />
      </section>
      <div className="dashboard-grid">
        <section className="panel activity-panel"><PanelTitle icon={Activity} title="آخر المستجدات" action="عرض السجل" /><div className="activity-list">
          <ActivityRow icon={Check} color="mint" title="تم اعتماد توفر متطوعين لفعالية يوم الذكاء الاصطناعي" meta="قبل ١٢ دقيقة · لجنة الأنشطة المتخصصة" />
          <ActivityRow icon={MessageSquareText} color="violet" title="أُضيفت ملاحظة مشاركة في ملف سارة منصور" meta="قبل ساعة · لجنة الإعلام" />
          <ActivityRow icon={CalendarDays} color="blue" title="فعالية جديدة بانتظار مراجعة نائب الرئيس" meta="قبل ٣ ساعات · لجنة الأنشطة" />
        </div></section>
        <section className="panel upcoming-panel"><PanelTitle icon={CalendarDays} title="الفعالية القادمة" action="كل الفعاليات" onAction={() => changeView('events')} /><div className="upcoming-card"><div className="upcoming-visual"><span className="date-pill">٢٨ أكتوبر</span><div className="visual-orbit" /><Sparkles size={34} /></div><div className="upcoming-info"><span className="tag tag-purple">لقاء مجتمعي</span><h3>يوم الذكاء الاصطناعي</h3><p><Clock3 size={14} /> الثلاثاء · ٩:٠٠ ص – ٤:٠٠ م</p><div className="avatar-stack"><Avatar initials="سم"/><Avatar initials="أخ" tone="blue"/><Avatar initials="لع" tone="pink"/><span>+١٨ متطوعاً</span></div><button className="text-action" onClick={() => changeView('events')}>إدارة التوفر <ArrowLeft size={14}/></button></div></div></section>
      </div>
      <section className="section-block"><PanelTitle icon={UsersRound} title="لجان ناي" subtitle="نظرة سريعة على فرق الجمعية" action="عرض كل اللجان" onAction={() => changeView('committees')} /><div className="committee-grid">{committees.map((item) => <CommitteeCard key={item.name} committee={item} onClick={() => { setActiveCommittee(item.name); changeView('committees') }} />)}</div></section>
    </>
  }

  function renderEvents() {
    return <div className="content-stack"><section className="event-heading-card"><div><span className="tag tag-purple">الثلاثاء · ٢٨ أكتوبر ٢٠٢٦</span><h2>يوم الذكاء الاصطناعي</h2><p>حدّد أوقات توفرك؛ مسؤول الفعالية يؤكد توزيعك على الفترة المناسبة.</p></div><button className="button button-outline" onClick={() => notify('نموذج إنشاء فعالية جديد جاهز للربط بالباك اند')}><Plus size={16}/> فعالية جديدة</button></section>
      <div className="availability-layout"><section className="panel slots-panel"><PanelTitle icon={CalendarDays} title="الفترات التطوعية" subtitle="نحتاج ١٤ متطوعاً لتغطية الفعالية" /><div className="legend"><span><i className="dot dot-mint"/> متاح</span><span><i className="dot dot-purple"/> تم التأكيد</span><span><i className="dot dot-pink"/> بحاجة لمتطوعين</span></div><div className="shift-list">{shifts.map((shift) => <div className={`shift-card shift-${shift.tint}`} key={shift.id}><div className="shift-icon"><Clock3 size={18}/></div><div className="shift-description"><strong>{shift.title}</strong><small>{shift.time}</small></div><div className="shift-coverage"><div className="coverage-line"><span style={{ width: `${Math.min(100, shift.assigned / shift.need * 100)}%` }} /></div><small className={shift.assigned < shift.need ? 'shortage' : ''}>{shift.assigned} من {shift.need} متطوعين</small></div><div className="avatar-stack shift-avatars">{shift.people.map((person, i) => <Avatar key={person + i} initials={person} tone={i % 3 === 0 ? 'purple' : i % 3 === 1 ? 'blue' : 'pink'} />)}</div><button className={`icon-button ${selected.includes(shift.id) ? 'is-selected' : ''}`} aria-label={`اختيار فترة ${shift.title}`} onClick={() => { setSelected((old) => old.includes(shift.id) ? old.filter((id) => id !== shift.id) : [...old, shift.id]); setSavedAvailability(false) }}>{selected.includes(shift.id) ? <Check size={17}/> : <Plus size={17}/>}</button></div>)}</div></section>
      <aside className="panel availability-form"><div className="form-heading"><div className="form-icon"><CalendarDays size={20}/></div><div><h3>متى أنت متاح؟</h3><p>اختَر الفترات التي تستطيع المشاركة فيها</p></div></div><div className="selected-count">الفترات المحددة <b>{selected.length}</b></div><div className="availability-options">{shifts.map((shift) => <button className={`availability-option ${selected.includes(shift.id) ? 'option-checked' : ''}`} key={shift.id} onClick={() => { setSelected((old) => old.includes(shift.id) ? old.filter((id) => id !== shift.id) : [...old, shift.id]); setSavedAvailability(false) }}><span className="check-box">{selected.includes(shift.id) && <Check size={14}/>}</span><span><b>{shift.title}</b><small>{shift.time}</small></span><span className={`mini-tag ${shift.assigned < shift.need ? 'mini-short' : 'mini-ok'}`}>{shift.assigned < shift.need ? `نحتاج ${shift.need - shift.assigned}` : 'مكتملة'}</span></button>)}</div><label className="field-label" htmlFor="availability-note">ملاحظة للمسؤول <small>اختياري</small></label><textarea id="availability-note" placeholder="مثلاً: أستطيع المساعدة في التصوير أو التسجيل" rows={3}/><button className="button button-primary button-wide" onClick={() => { setSavedAvailability(true); notify('تم إرسال أوقات توفرك للمراجعة') }}>{savedAvailability ? <><Check size={17}/> تم إرسال التوفر</> : <>حفظ أوقات التوفر <ArrowLeft size={17}/></>}</button><p className="form-footnote">إرسال التوفر لا يعني تأكيد مشاركتك. سيصلك إشعار بعد اعتماد الفترة.</p></aside></div>
      <section className="panel confirmed-panel"><PanelTitle icon={ShieldCheck} title="التوزيع المؤكد" subtitle="المتطوعون الذين تم تأكيد مشاركتهم" action="تصدير القائمة" /><div className="confirmed-list">{[
        ['سارة منصور','لجنة الإعلام','التجهيز · ٨:٠٠ – ٩:٣٠ ص','سم'],['أحمد خالد','لجنة التقنية','تنظيم القاعة · ١٢:٠٠ – ٢:٠٠ م','أخ'],['ليان عودة','لجنة الأنشطة','الاستقبال · ٩:٣٠ ص – ١٢:٠٠ م','لع'],
      ].map(([name, committee, shift, initials]) => <div className="confirmed-row" key={name}><Avatar initials={initials}/><b>{name}</b><span>{committee}</span><span className="confirmed-shift"><Clock3 size={14}/>{shift}</span><span className="status-chip status-confirmed"><Check size={13}/> مؤكد</span></div>)}</div></section>
    </div>
  }

  function renderCommittees() {
    return <div className="content-stack"><section className="filter-row"><div><h2>فرق ناي تعمل معاً</h2><p>كل لجنة تتابع متطوعيها ومشاركتهم في الفعاليات.</p></div><button className="button button-primary" onClick={() => notify('إضافة لجنة تتطلب صلاحية الهيئة الإدارية')}><Plus size={16}/> إضافة لجنة</button></section><div className="committee-grid committee-grid-large">{committees.map((item) => <CommitteeCard key={item.name} committee={item} onClick={() => { setActiveCommittee(item.name); changeView('volunteers') }} expanded />)}</div><section className="panel"><PanelTitle icon={UsersRound} title="مسؤولو اللجان"/><div className="lead-grid">{committees.slice(0, 4).map((item, index) => <div className="lead-card" key={item.name}><Avatar initials={['سم','أخ','لع','من'][index]} tone={['pink','blue','purple','mint'][index]}/><div><b>{['سارة منصور','أحمد خالد','ليان عودة','محمد ناصر'][index]}</b><small>{item.name}</small></div><ShieldCheck size={17} className="lead-check"/></div>)}</div></section></div>
  }

  function renderVolunteers() {
    return <div className="content-stack"><section className="filter-row"><div><h2>ملفات المتطوعين</h2><p>الملاحظات والتقييمات محفوظة ضمن اللجنة التي أضافتها.</p></div><button className="button button-outline" onClick={() => notify('تم تجهيز قائمة المتطوعين للتصدير')}><Download size={16}/> تصدير</button></section><div className="filter-chips">{['الكل', ...committees.map((item) => item.name)].map((name) => <button className={activeCommittee === name ? 'filter-chip active' : 'filter-chip'} key={name} onClick={() => setActiveCommittee(name)}>{name}</button>)}</div><section className="volunteer-grid">{filteredVolunteers.map((person) => <article className="panel volunteer-card" key={person.name}><div className="volunteer-card-top"><Avatar initials={person.initials}/><span className="status-chip status-active"><i/> نشط</span></div><h3>{person.name}</h3><span className="tag tag-soft">{person.committee}</span><div className="volunteer-stats"><div><b>{person.events}</b><small>مشاركات</small></div><div><b>{person.hours}</b><small>ساعة تطوع</small></div></div><div className="note-preview"><MessageSquareText size={15}/><p>{person.note}</p></div><button className="text-action" onClick={() => { setActiveCommittee(person.committee); setView('evaluations') }}>فتح الملف والتقييم <ArrowLeft size={14}/></button></article>)}</section></div>
  }

  function renderEvaluations() {
    return <div className="evaluation-layout"><section className="content-stack"><div className="panel evaluation-profile"><div className="profile-avatar"><Avatar initials="سم"/></div><div className="profile-details"><span className="tag tag-purple">لجنة الإعلام</span><h2>سارة منصور</h2><p>متطوعة نشطة · ٨ مشاركات في فعاليات الجمعية</p></div><button className="button button-outline" onClick={() => notify('ملف المتطوعة يعرض تاريخ المشاركة والملاحظات')} >ملف المشاركة <ChevronLeft size={15}/></button></div><div className="panel"><PanelTitle icon={Star} title="تقييم الفصل" subtitle="التقييم يخص مشاركة المتطوعة مع لجنة الإعلام" action="الموسم الحالي"/><div className="rating-grid">{[['المشاركة','4.8'],['جودة المساهمة','4.5'],['الالتزام','4.8'],['التعاون','4.6'],['المبادرة','4.4']].map(([name, score]) => <div className="rating-item" key={name}><div className="rating-ring"><b>{score}</b><small>/ ٥</small></div><span>{name}</span></div>)}</div><div className="evaluation-summary"><Sparkles size={17}/><p><b>نقطة قوة:</b> مبادرة واضحة في تغطية الفعاليات والتعاون مع الفريق.<br/><b>خطوة قادمة:</b> تأكيد الفترات المناسبة مبكراً لتسهيل التوزيع.</p></div><div className="evaluation-footer"><span className="status-chip status-review"><Clock3 size={13}/> بانتظار مراجعة مسؤول المتطوعين</span><button className="button button-primary" onClick={() => notify('أُرسل التقييم للمراجعة')}>إرسال للمراجعة <ArrowLeft size={15}/></button></div></div></section><aside className="panel note-compose"><div className="form-heading"><span className="form-icon"><MessageSquareText size={20}/></span><div><h3>ملاحظة اللجنة</h3><p>اربط الملاحظة بمشاركة محددة وخلّيها بنّاءة.</p></div></div><label className="field-label" htmlFor="event-note">الفعالية المرتبطة</label><select id="event-note" defaultValue="يوم الذكاء الاصطناعي"><option>يوم الذكاء الاصطناعي</option><option>ورشة تعلم الآلة</option><option>لقاء المجتمع التقني</option></select><label className="field-label" htmlFor="note-input">الملاحظة</label><textarea id="note-input" rows={5} value={noteText} onChange={(event) => setNoteText(event.target.value)} placeholder="مثال: تميّزتِ في استقبال الضيوف وساعدتِ الفريق في تغطية الفعالية..."/><p className="privacy-note"><ShieldCheck size={15}/> تظهر الملاحظة للمتطوعة ومسؤولي المتابعة المخوّلين فقط.</p><button className="button button-primary button-wide" onClick={saveNote}>حفظ الملاحظة <ArrowLeft size={16}/></button>{savedNote && <div className="saved-note"><Check size={14}/><span>آخر ملاحظة محفوظة: {savedNote}</span></div>}</aside></div>
  }

  function renderFinance() {
    return <div className="content-stack"><section className="finance-welcome panel"><div className="finance-orb"><Coins size={26}/></div><div><span className="tag tag-purple">صلاحية مسؤول الصندوق</span><h2>السجل المالي للجمعية</h2><p>الوصول لهذه الصفحة مخصص لمسؤول الصندوق والرئيس، مع تسجيل كل تعديل.</p></div><button className="button button-primary" onClick={() => notify('أُضيفت واجهة تسجيل معاملة جديدة للتصميم')}><Plus size={16}/> معاملة جديدة</button></section><div className="stat-grid finance-stats"><StatCard icon={ArrowDownLeft} label="إيرادات الفصل" value="₪ 3,250" delta="محدّثة حتى اليوم" tone="mint"/><StatCard icon={ArrowUpLeft} label="مصروفات الفصل" value="₪ 1,480" delta="١٢ معاملة مسجلة" tone="pink"/><StatCard icon={Wallet} label="الرصيد الحالي" value="₪ 1,770" delta="حسب السجل المعتمد" tone="purple"/><StatCard icon={ShieldCheck} label="بانتظار الاعتماد" value="03" delta="تحتاج مراجعة الرئيس" tone="blue"/></div><section className="panel"><PanelTitle icon={Coins} title="آخر المعاملات" action="تصدير التقرير"/><div className="table-wrap"><table><thead><tr><th>التاريخ</th><th>البيان</th><th>التصنيف</th><th>النوع</th><th>المبلغ</th><th>الحالة</th></tr></thead><tbody>{[['٢٠ أكتوبر','مواد لوجستية للورشة','فعاليات','مصروف','₪ ٣٢٠','معتمد'],['١٨ أكتوبر','دعم من شريك مجتمعي','دعم','إيراد','₪ ٨٠٠','معتمد'],['١٥ أكتوبر','طباعة مواد تعريفية','إعلام','مصروف','₪ ١٦٠','بانتظار الاعتماد']].map((row) => <tr key={row[1]}>{row.map((cell, index) => <td key={index}>{index === 5 ? <span className={`status-chip ${cell === 'معتمد' ? 'status-confirmed' : 'status-review'}`}>{cell}</span> : cell}</td>)}</tr>)}</tbody></table></div></section></div>
  }

  return <div className="app-shell">
    <aside className={`sidebar ${mobileOpen ? 'sidebar-open' : ''}`}><div className="sidebar-brand"><Brand/><button className="close-sidebar" onClick={() => setMobileOpen(false)} aria-label="إغلاق القائمة"><X size={18}/></button></div><div className="sidebar-label">مساحة الجمعية</div><nav className="side-nav">{nav.map(({ id, label, icon: Icon }) => <button className={view === id ? 'nav-item nav-active' : 'nav-item'} key={id} onClick={() => changeView(id)}><Icon size={18}/><span>{label}</span>{id === 'evaluations' && <i className="nav-badge">٣</i>}</button>)}</nav><div className="sidebar-spacer"/><div className="sidebar-committee"><span className="committee-orb"><Sparkles size={17}/></span><div><b>جمعية ناي</b><small>جامعة النجاح الوطنية</small></div><ChevronDown size={15}/></div><button className="nav-item settings-item" onClick={() => notify('إعدادات المنصة ستُتاح للمسؤولين')}><Settings2 size={18}/><span>الإعدادات</span></button><div className="sidebar-user"><Avatar initials="سم"/><div><b>سارة منصور</b><small>مسؤولة لجنة الإعلام</small></div><ChevronDown size={15}/></div></aside>
    {mobileOpen && <button className="mobile-scrim" aria-label="إغلاق القائمة" onClick={() => setMobileOpen(false)}/>}
    <main className="main-area"><header className="topbar"><button className="mobile-menu" onClick={() => setMobileOpen(true)} aria-label="فتح القائمة"><Menu size={21}/></button><div className="breadcrumb"><span>جمعية ناي</span><ChevronLeft size={15}/><b>{nav.find((item) => item.id === view)?.label}</b></div><div className="topbar-actions"><label className="search-box"><Search size={16}/><input aria-label="بحث" placeholder="ابحث عن متطوع أو فعالية..."/><kbd>⌘ K</kbd></label><button className="button button-outline register-button" onClick={() => { setAuthMode('login'); setRegisterError(''); setRegisterOpen(true) }}>تسجيل الدخول</button><button className="button button-primary register-button" onClick={() => { setAuthMode('register'); setRegisterError(''); setRegisterOpen(true) }}><UserRoundPlus size={15}/> إنشاء حساب</button><button className="icon-button notification-button" aria-label="الإشعارات"><Bell size={18}/><i/></button><div className="top-avatar"><Avatar initials="سم"/><span><b>سارة منصور</b><small>الهيئة الإدارية</small></span><ChevronDown size={14}/></div></div></header>
      <div className="page-content"><section className="page-heading"><div><span className="eyebrow"><span className="live-dot"/> منصة مجتمع ناي</span><h1>{heading[0]}</h1><p>{heading[1]}</p></div>{view === 'overview' && <button className="button button-outline" onClick={() => notify('تم تجهيز ملخص الجمعية للتصدير')}><Download size={16}/> تصدير الملخص</button>}</section>{view === 'overview' ? renderOverview() : view === 'events' ? renderEvents() : view === 'committees' ? renderCommittees() : view === 'volunteers' ? renderVolunteers() : view === 'evaluations' ? renderEvaluations() : renderFinance()}</div>
      <footer className="footer"><span>© ٢٠٢٦ جمعية ناي للذكاء الاصطناعي</span><span><i/> كل اللجان تعمل ضمن مساحة واحدة</span></footer>
    </main>
    {registerOpen && <div className="modal-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) setRegisterOpen(false) }}><section className="register-modal" role="dialog" aria-modal="true" aria-labelledby="register-title"><div className="modal-top"><div><span className="tag tag-purple">{authMode === 'register' ? 'إنشاء حساب' : 'دخول آمن'}</span><h2 id="register-title">{authMode === 'register' ? 'اطلب الانضمام إلى منصة ناي' : 'تسجيل الدخول إلى ناي'}</h2><p>{authMode === 'register' ? 'باب الانتساب للجمعية مغلق؛ هذا الطلب للتحقق من سجلك ودورك الحالي.' : 'الحسابات الإدارية تتاح بعد اعتماد بيانات العضوية والدور.'}</p></div><button className="icon-button" onClick={() => setRegisterOpen(false)} aria-label="إغلاق"><X size={17}/></button></div><form onSubmit={(event) => { event.preventDefault(); void submitRegistration(event.currentTarget) }}><div className="register-fields">{authMode === 'register' ? <><label>الاسم الأول<input name="first_name" required autoComplete="given-name"/></label><label>اسم العائلة<input name="last_name" autoComplete="family-name"/></label><label>البريد الإلكتروني<input name="email" type="email" required autoComplete="email"/></label><label>اسم المستخدم<input name="username" required autoComplete="username"/></label><label>الرقم الجامعي<input name="university_id" required/></label><label>رقم الهاتف<input name="phone" type="tel"/></label><label>كلمة المرور<input name="password" type="password" minLength={10} required autoComplete="new-password"/></label><label>الدور المطلوب<select name="requested_role" value={registerRole} onChange={(event) => setRegisterRole(event.target.value)}><option value="member">منتسب</option><option value="volunteer">متطوع</option><option value="committee_lead">مسؤول لجنة</option><option value="volunteer_manager">مسؤول المتطوعين</option><option value="vice_president">نائب الرئيس</option><option value="president">الرئيس</option><option value="treasurer">مسؤول الصندوق</option></select></label>{['volunteer','committee_lead'].includes(registerRole) && <label className="field-full">اللجنة المطلوبة<select name="requested_committee" required defaultValue=""><option value="" disabled>اختر اللجنة</option>{committees.map((committee) => <option key={committee.name} value={committee.name}>{committee.name}</option>)}</select></label>}</> : <><label className="field-full">اسم المستخدم<input name="username" required autoComplete="username"/></label><label className="field-full">كلمة المرور<input name="password" type="password" required autoComplete="current-password"/></label></>}</div>{authMode === 'register' && <div className="role-notice"><ShieldCheck size={16}/><span>اختيار الدور يرسل طلب تحقق فقط. لا تُمنح أي صلاحيات إدارية قبل اعتمادها من الهيئة الإدارية.</span></div>}{registerError && <p className="register-error" role="alert">{registerError}</p>}<button className="button button-primary button-wide" disabled={registerBusy}>{registerBusy ? 'جارٍ الإرسال…' : authMode === 'register' ? <>إرسال طلب التحقق <ArrowLeft size={16}/></> : <>تسجيل الدخول <ArrowLeft size={16}/></>}</button><button type="button" className="auth-switch" onClick={() => { setAuthMode(authMode === 'register' ? 'login' : 'register'); setRegisterError('') }}>{authMode === 'register' ? 'عندك حساب؟ سجّل الدخول' : 'ما عندك حساب؟ اطلب إنشاء حساب'}</button></form></section></div>}
    {toast && <div className="toast"><Check size={17}/>{toast}</div>}
  </div>
}

function StatCard({ icon: Icon, label, value, delta, tone }: { icon: typeof UsersRound; label: string; value: string; delta: string; tone: string }) {
  return <article className="stat-card"><div className={`stat-icon tone-${tone}`}><Icon size={19}/></div><div className="stat-copy"><small>{label}</small><strong>{value}</strong><span>{delta}</span></div><div className="stat-spark"><span/><span/><span/><span/><span/></div></article>
}

function PanelTitle({ icon: Icon, title, subtitle, action, onAction }: { icon: typeof UsersRound; title: string; subtitle?: string; action?: string; onAction?: () => void }) {
  return <div className="panel-title"><div className="title-icon"><Icon size={17}/></div><div><h3>{title}</h3>{subtitle && <p>{subtitle}</p>}</div>{action && <button className="text-action panel-action" onClick={onAction}>{action}<ArrowLeft size={14}/></button>}</div>
}

function ActivityRow({ icon: Icon, color, title, meta }: { icon: typeof Check; color: string; title: string; meta: string }) {
  return <div className="activity-row"><span className={`activity-icon tone-${color}`}><Icon size={16}/></span><div><b>{title}</b><small>{meta}</small></div><span className="activity-time">الآن</span></div>
}

function CommitteeCard({ committee, onClick, expanded = false }: { committee: Committee; onClick: () => void; expanded?: boolean }) {
  return <button className={`committee-card committee-${committee.color} ${expanded ? 'committee-expanded' : ''}`} onClick={onClick}><div className="committee-card-top"><span className="committee-icon">{committee.icon}</span><span className="committee-members"><UsersRound size={14}/>{committee.count}</span></div><h3>{committee.name}</h3><p>{committee.note}</p><div className="committee-progress"><span style={{ width: `${38 + committee.count * 3}%` }}/></div><div className="committee-card-foot"><span>{committee.count} متطوعاً</span><span>فتح اللجنة <ArrowLeft size={13}/></span></div></button>
}

export default App
