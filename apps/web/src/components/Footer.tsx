// Using inline SVGs for social icons as Lucide-react removed brand icons

export default function Footer() {
  return (
    <footer className="bg-[#0f0f0f] text-white pt-20 pb-8 px-8 border-t border-neutral-900">
      <div className="container mx-auto max-w-6xl">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
          
          {/* Column 1: Brand & Newsletter */}
          <div className="md:col-span-2">
            <h2 className="text-3xl font-bold tracking-tight mb-4 text-white">FitCore</h2>
            <p className="text-gray-400 text-sm mb-10 max-w-sm leading-relaxed">
              Um Lugar Onde a Força e a<br/>Comunidade Crescem Juntas
            </p>
            
            <form className="max-w-md">
              <div className="mb-4">
                <input 
                  type="email" 
                  placeholder="Seu Endereço de E-mail" 
                  className="w-full bg-transparent border-b border-neutral-800 pb-3 text-sm focus:outline-none focus:border-white transition-colors text-white placeholder-neutral-600"
                />
              </div>
              <button 
                type="submit"
                className="bg-white text-black text-xs font-bold uppercase tracking-widest px-8 py-3 hover:bg-emerald-500 hover:text-white transition-colors mt-2"
              >
                Inscrever-se
              </button>
            </form>
          </div>

          {/* Column 2: Services */}
          <div>
            <h4 className="text-lg font-medium mb-6">Serviços</h4>
            <ul className="space-y-4 text-sm text-gray-400">
              <li><a href="#" className="hover:text-white transition-colors">Personal Training</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Aulas em Grupo</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Força e Condicionamento</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Treinamento Cardio</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Treinamento Funcional</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Bem-Estar e Recuperação</a></li>
            </ul>
          </div>

          {/* Column 3: Contacts */}
          <div>
            <h4 className="text-lg font-medium mb-6">Contatos</h4>
            <ul className="space-y-4 text-sm text-gray-400 mb-8">
              <li>27 Division St, New York,<br/>NY 10002, USA</li>
              <li><a href="tel:+1800123456789" className="hover:text-white transition-colors">+1 800 123 456 789</a></li>
              <li><a href="mailto:synta@mail.com" className="hover:text-white transition-colors">synta@mail.com</a></li>
            </ul>
            
            {/* Social Icons */}
            <div className="flex gap-2">
              <a href="#" className="w-10 h-10 border border-neutral-800 flex items-center justify-center hover:bg-white hover:text-black transition-colors">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>
              </a>
              <a href="#" className="w-10 h-10 border border-neutral-800 flex items-center justify-center hover:bg-white hover:text-black transition-colors">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
              </a>
              <a href="#" className="w-10 h-10 bg-white text-black flex items-center justify-center hover:bg-gray-200 transition-colors">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
              </a>
            </div>
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-neutral-900 flex flex-col md:flex-row justify-between items-center text-xs text-neutral-600">
          <p>Copyright © 2026 FitCore. Todos os Direitos Reservados.</p>
          <div className="flex gap-8 mt-4 md:mt-0">
            <a href="#" className="hover:text-white transition-colors">Termos de Uso</a>
            <a href="#" className="hover:text-white transition-colors">Política de Privacidade</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
