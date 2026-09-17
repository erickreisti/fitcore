export default function CoachesSection() {
  const coaches = [
    { name: "Matey Black", role: "TREINADOR PRINCIPAL", image: "https://images.unsplash.com/photo-1567598508481-65985588e295?q=80&w=2070&auto=format&fit=crop" },
    { name: "Christian Grant", role: "PERSONAL TRAINER", image: "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?q=80&w=2070&auto=format&fit=crop" },
    { name: "Sandra Lee", role: "INSTRUTORA DE FITNESS", image: "https://images.unsplash.com/photo-1548690312-e3b507d8c110?q=80&w=2070&auto=format&fit=crop" },
    { name: "Mary Petterson", role: "TREINADORA DE GRUPOS", image: "https://images.unsplash.com/photo-1609899517236-77f646b96e57?q=80&w=2070&auto=format&fit=crop" },
  ];

  return (
    <section className="bg-[#111111] text-white py-24 px-8">
      <div className="container mx-auto max-w-5xl">
        
        {/* Header */}
        <div className="mb-16">
          <span className="text-xs font-bold uppercase tracking-widest text-neutral-500 mb-6 block">
            ( TREINADORES QUE TRAZEM RESULTADOS )
          </span>
          <h2 className="text-4xl md:text-5xl font-medium tracking-tight max-w-xl leading-tight">
            Nossos Especialistas Dedicados ao Seu Sucesso
          </h2>
        </div>

        {/* Coaches List */}
        <div className="border-t border-neutral-800 mb-24">
          {coaches.map((coach, index) => (
            <div 
              key={index}
              className="group relative flex flex-col md:flex-row md:items-center justify-between py-10 border-b border-neutral-800 transition-colors hover:bg-neutral-900/50"
            >
              <div className="flex items-baseline gap-4 relative z-10 pl-4 md:pl-0">
                <h3 className="text-3xl md:text-5xl font-medium text-neutral-400 group-hover:text-white transition-colors">
                  {coach.name}
                </h3>
                <span className="text-xs tracking-widest text-neutral-600 uppercase font-bold">
                  / {coach.role}
                </span>
              </div>

              {/* Hover Image (Hidden by default, appears on hover in center) */}
              <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none hidden md:block">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img 
                  src={coach.image} 
                  alt={coach.name} 
                  className="w-64 h-64 object-cover shadow-2xl grayscale group-hover:grayscale-0 transition-all duration-500"
                />
              </div>

              <div className="relative z-10 mt-6 md:mt-0 pr-4 md:pr-0 self-start md:self-auto">
                <a 
                  href="#" 
                  className="inline-block border border-neutral-700 text-xs font-bold tracking-widest uppercase px-8 py-3 text-neutral-400 group-hover:bg-white group-hover:text-black group-hover:border-white transition-all"
                >
                  Ver Mais
                </a>
              </div>
            </div>
          ))}
        </div>

        {/* Stats Footer */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 text-center md:text-left">
          
          <div className="flex items-center justify-center md:justify-start gap-4">
            <span className="text-6xl md:text-7xl font-bold text-neutral-700">150+</span>
            <span className="text-sm font-medium leading-tight">Clientes<br/>Ativos</span>
          </div>

          <div className="flex items-center justify-center md:justify-start gap-4">
            <span className="text-6xl md:text-7xl font-bold text-neutral-700">34</span>
            <span className="text-sm font-medium leading-tight">Treinadores<br/>Qualificados</span>
          </div>

          <div className="flex items-center justify-center md:justify-start gap-4">
            <span className="text-6xl md:text-7xl font-bold text-neutral-700">240</span>
            <span className="text-sm font-medium leading-tight">Metros<br/>Quadrados</span>
          </div>

        </div>

      </div>
    </section>
  );
}
