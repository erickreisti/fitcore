import { Dumbbell01Icon, Medal01Icon, Activity01Icon } from "hugeicons-react";

export default function FeaturesCards() {
  return (
    <section className="bg-neutral-950 text-white py-24 px-8 relative overflow-hidden">
      
      {/* Background massive typography */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full text-center whitespace-nowrap opacity-[0.03] pointer-events-none">
        <h2 className="text-[150px] font-bold tracking-tighter">Compromisso encontra resultados</h2>
      </div>

      <div className="container mx-auto max-w-6xl relative z-10">
        
        {/* Header */}
        <div className="text-center mb-16">
          <span className="text-xs uppercase tracking-widest text-gray-400 mb-6 block">( MAIS QUE UMA ACADEMIA )</span>
          <h3 className="text-4xl md:text-5xl font-light text-gray-400 leading-tight max-w-3xl mx-auto">
            Nosso espaço combina <strong className="text-white font-semibold">equipamentos profissionais</strong>, treinadores especializados e uma atmosfera motivadora para ajudar você a <strong className="text-white font-semibold">treinar com inteligência</strong>, mover-se melhor e ficar mais forte — <strong className="text-white font-semibold">todos os dias.</strong>
          </h3>
        </div>

        {/* 3 Columns */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          {/* Card 1 */}
          <div className="bg-[#111] p-10 border border-neutral-800/50 hover:bg-[#161616] hover:border-emerald-900/30 transition-colors group">
            <div className="w-14 h-14 bg-neutral-800 mb-8 flex items-center justify-center group-hover:bg-emerald-500 group-hover:text-black transition-colors">
              <Medal01Icon className="w-6 h-6 text-emerald-400 group-hover:text-black" />
            </div>
            <h4 className="text-xl font-bold mb-4">Treinamento Profissional</h4>
            <p className="text-gray-400 text-sm leading-relaxed">
              Treine com instrutores certificados que criam programas estruturados baseados nos seus objetivos, nível de condicionamento e progresso.
            </p>
          </div>

          {/* Card 2 */}
          <div className="bg-[#111] p-10 border border-neutral-800/50 hover:bg-[#161616] hover:border-emerald-900/30 transition-colors group">
            <div className="w-14 h-14 bg-neutral-800 mb-8 flex items-center justify-center group-hover:bg-emerald-500 group-hover:text-black transition-colors">
              <Dumbbell01Icon className="w-6 h-6 text-emerald-400 group-hover:text-black" />
            </div>
            <h4 className="text-xl font-bold mb-4">Equipamentos Modernos</h4>
            <p className="text-gray-400 text-sm leading-relaxed">
              Nossa academia é equipada com máquinas de última geração e áreas de treinamento funcional que suportam força e mobilidade.
            </p>
          </div>

          {/* Card 3 */}
          <div className="bg-[#111] p-10 border border-neutral-800/50 hover:bg-[#161616] hover:border-emerald-900/30 transition-colors group">
            <div className="w-14 h-14 bg-neutral-800 mb-8 flex items-center justify-center group-hover:bg-emerald-500 group-hover:text-black transition-colors">
              <Activity01Icon className="w-6 h-6 text-emerald-400 group-hover:text-black" />
            </div>
            <h4 className="text-xl font-bold mb-4">Ambiente Motivador</h4>
            <p className="text-gray-400 text-sm leading-relaxed">
              Treine em uma atmosfera energética, limpa e acolhedora que mantém você inspirado e motivado.
            </p>
          </div>

        </div>
      </div>
    </section>
  );
}
