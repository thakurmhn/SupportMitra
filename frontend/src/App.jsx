const services = [
  { id: 'desktop', title: 'Desktop / Laptop Support', description: 'Remote troubleshooting, antivirus, and connectivity support.' },
  { id: 'linux', title: 'Linux Provisioning', description: 'Server setup, package management, and automation for Linux nodes.' },
  { id: 'windows', title: 'Windows Provisioning', description: 'Windows server deployment, Active Directory, and desktop rollout.' },
  { id: 'patching', title: 'OS Patching', description: 'Managed patching for Windows and Linux infrastructure.' },
  { id: 'security', title: 'Security Hardening', description: 'Baseline hardening, vulnerability remediation, and access control.' },
  { id: 'vmware', title: 'VMware / Hypervisor Support', description: 'Host management, VM provisioning, and storage troubleshooting.' },
  { id: 'sap', title: 'SAP Basis Lite', description: 'Support for SAP infrastructure, transports, and system health checks.' },
]

function App() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white shadow-sm">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-2xl font-semibold">SupportMitra</h1>
            <p className="text-sm text-slate-500">SMB IT support portal for servers, SAP, and infrastructure operations.</p>
          </div>
          <nav className="space-x-4 text-sm text-slate-700">
            <a href="/" className="font-medium hover:text-slate-900">Home</a>
            <a href="#services" className="hover:text-slate-900">Services</a>
            <a href="#signup" className="hover:text-slate-900">Get Started</a>
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-6 py-12">
        <section className="rounded-3xl bg-slate-900 px-8 py-12 text-white shadow-xl sm:px-10">
          <h2 className="text-4xl font-semibold tracking-tight">IT support for SMBs and small SAP shops.</h2>
          <p className="mt-4 max-w-2xl text-lg text-slate-200">
            Fast ticket-based support, transparent pricing, and a freelancer admin backend built for low-cost deployment.
          </p>
          <div className="mt-8 flex flex-col gap-4 sm:flex-row">
            <a href="#signup" className="inline-flex items-center justify-center rounded-full bg-emerald-500 px-6 py-3 text-sm font-semibold text-white shadow hover:bg-emerald-400">Open a support case</a>
            <a href="/admin/" className="inline-flex items-center justify-center rounded-full border border-white/20 bg-white/10 px-6 py-3 text-sm font-semibold text-white hover:bg-white/20">Freelancer login</a>
          </div>
        </section>

        <section id="services" className="mt-16">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-3xl font-semibold">Service categories</h3>
              <p className="mt-2 text-slate-600">Core offerings for server operations, security, and SAP Basis support.</p>
            </div>
          </div>
          <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {services.map((service) => (
              <article key={service.id} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
                <h4 className="text-xl font-semibold">{service.title}</h4>
                <p className="mt-3 text-slate-600">{service.description}</p>
              </article>
            ))}
          </div>
        </section>

        <section id="signup" className="mt-20 rounded-3xl bg-white p-8 shadow-sm sm:p-10">
          <h3 className="text-3xl font-semibold">Pilot launch checklist</h3>
          <ul className="mt-6 grid gap-4 text-slate-700 sm:grid-cols-2">
            <li className="rounded-2xl border border-slate-200 bg-slate-50 p-5">Define support packages and pricing</li>
            <li className="rounded-2xl border border-slate-200 bg-slate-50 p-5">Build signup, payment, and ticket workflows</li>
            <li className="rounded-2xl border border-slate-200 bg-slate-50 p-5">Integrate Razorpay / PayU for ₹299 fee</li>
            <li className="rounded-2xl border border-slate-200 bg-slate-50 p-5">Launch pilot with first SMB customers</li>
          </ul>
        </section>
      </main>
    </div>
  )
}

export default App
