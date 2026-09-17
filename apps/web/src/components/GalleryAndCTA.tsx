import { ArrowLeft01Icon, ArrowRight01Icon } from "hugeicons-react";

export default function GalleryAndCTA() {
  const galleryItems = [
    { title: "Treino Pessoal", category: "TREINAMENTO - ACADEMIA", image: "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?q=80&w=2070&auto=format&fit=crop" },
    { title: "Equipamentos", category: "TREINAMENTO - ACADEMIA", image: "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?q=80&w=2071&auto=format&fit=crop" },
    { title: "Treino em Grupo", category: "TREINAMENTO - ACADEMIA", image: "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=2070&auto=format&fit=crop" },
    { title: "Máquinas", category: "TREINAMENTO - ACADEMIA", image: "https://images.unsplash.com/photo-1540497077202-7c8a3999166f?q=80&w=2070&auto=format&fit=crop" },
  ];

  return (
    <section className="bg-[#161616] text-white pt-24 overflow-hidden relative">
      
      {/* Gallery Carousel Section */}
      <div className="w-full mb-32 px-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {galleryItems.map((item, index) => (
            <div key={index} className="group cursor-pointer">
              {/* Image Container */}
              <div className="overflow-hidden mb-6 bg-neutral-800 aspect-4/5 relative">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img 
                  src={item.image} 
                  alt={item.title} 
                  className="w-full h-full object-cover grayscale group-hover:grayscale-0 group-hover:scale-105 transition-all duration-700"
                />
              </div>
              {/* Text */}
              <h3 className="text-xl font-medium mb-1">{item.title}</h3>
              <p className="text-[10px] text-neutral-500 uppercase tracking-widest font-bold">
                {item.category}
              </p>
            </div>
          ))}
        </div>

        {/* Carousel Arrows */}
        <div className="flex justify-center items-center gap-6 mt-12 text-neutral-500">
          <button className="hover:text-white transition-colors">
            <ArrowLeft01Icon className="w-5 h-5" />
          </button>
          <button className="hover:text-white transition-colors">
            <ArrowRight01Icon className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Become a Member CTA Section */}
      <div className="relative w-full py-40 flex flex-col items-center justify-center bg-[#111111]">
        
        {/* Background Outline Text (e.g. "X2") */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-[350px] font-black text-transparent opacity-[0.02] pointer-events-none select-none leading-none tracking-tighter"
             style={{ WebkitTextStroke: "2px rgba(255,255,255,1)" }}>
          X2
        </div>

        {/* Foreground Content */}
        <div className="relative z-10 text-center">
          <h2 className="text-6xl md:text-8xl font-medium tracking-tight mb-8">
            Seja um Membro
          </h2>
        </div>

        {/* Floating Circular Button */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 mt-16 z-20">
          <a href="#" className="w-32 h-32 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center text-white text-[10px] uppercase font-bold tracking-widest border border-white/30 hover:bg-emerald-500 hover:border-emerald-500 hover:text-black hover:scale-110 transition-all duration-300 shadow-2xl">
            Saiba Mais
          </a>
        </div>
      </div>

    </section>
  );
}
