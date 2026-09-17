"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { PlayIcon, Cancel01Icon } from "hugeicons-react";

const slides = [
  {
    video: "/videos/funcional.mp4",
    title: "Força.<br/>Resistência.<br/>Cardio.",
    service: "Treinamento Profissional",
    tag: "01 / 03",
    subtitle: "Um espaço construído para performance — equipamentos profissionais, metodologia inteligente e treinadores que se importam com o seu progresso."
  },
  {
    video: "/videos/fitness.mp4",
    title: "Foco.<br/>Poder.<br/>Resultados.",
    service: "Equipamentos Modernos",
    tag: "02 / 03",
    subtitle: "Máquinas biomecânicas de última geração, pesos livres e espaço funcional — tudo para você extrair o máximo de cada treino."
  },
  {
    video: "/videos/cardio.mp4",
    title: "Energia.<br/>Motivação.<br/>Comunidade.",
    service: "Aulas em Grupo",
    tag: "03 / 03",
    subtitle: "Aulas em grupo com música alta, instrutor presente e uma energia que você só encontra aqui. Venha sentir a diferença."
  }
];

const SLIDE_DURATION = 8000;

export default function HeroSection() {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [modalOpen, setModalOpen] = useState(false);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const startTimer = useCallback(() => {
    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, SLIDE_DURATION);
  }, []);

  useEffect(() => {
    startTimer();
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [startTimer]);

  useEffect(() => {
    document.body.style.overflow = modalOpen ? "hidden" : "";
    return () => { document.body.style.overflow = ""; };
  }, [modalOpen]);

  const handleIndicatorClick = (index: number) => {
    setCurrentSlide(index);
    startTimer();
  };

  return (
    <>
      {/* ── Video Modal ── */}
      {modalOpen && (
        <div
          className="fixed inset-0 z-100 bg-black/90 flex items-center justify-center"
          onClick={() => setModalOpen(false)}
        >
          <button
            className="absolute top-6 right-6 text-white hover:text-emerald-400 transition-colors"
            onClick={() => setModalOpen(false)}
          >
            <Cancel01Icon className="w-8 h-8" />
          </button>
          <video
            key={slides[currentSlide].video}
            controls
            autoPlay
            className="max-w-5xl w-full max-h-[80vh] rounded-lg shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <source src={slides[currentSlide].video} type="video/mp4" />
          </video>
        </div>
      )}

      {/* ── Hero ── */}
      <section className="relative w-full h-screen min-h-175 bg-black overflow-hidden flex flex-col">

        {/* Videos */}
        <div className="absolute inset-0 z-0">
          {slides.map((slide, index) => (
            <video
              key={index}
              autoPlay loop muted playsInline preload="auto"
              style={{ transition: "opacity 1.5s ease-in-out" }}
              className={`absolute inset-0 w-full h-full object-cover transition-opacity ${
                currentSlide === index ? "opacity-60" : "opacity-0"
              }`}
            >
              <source src={slide.video} type="video/mp4" />
            </video>
          ))}
        </div>

        {/* Overlays */}
        <div className="absolute inset-0 z-10 bg-linear-to-b from-black/60 via-black/20 to-black/80" />
        {/* Bottom fade into next section */}
        <div className="absolute bottom-0 left-0 right-0 h-56 z-10 bg-linear-to-t from-neutral-950 to-transparent" />

        {/* ── Top row: play + description ── */}
        <div className="relative z-20 w-full flex justify-between items-start px-8 pt-28">

          {/* Left: play button */}
          <div className="flex items-center gap-4 text-white">
            <button
              onClick={() => setModalOpen(true)}
              className="shrink-0 w-12 h-12 rounded-full border border-white/30 flex items-center justify-center hover:bg-emerald-500 hover:border-emerald-500 hover:text-black transition-all duration-300 hover:scale-110"
            >
              <PlayIcon className="w-4 h-4 ml-0.5" />
            </button>
            <p className="text-xs uppercase tracking-widest font-medium leading-relaxed text-white/70">
              {slides[currentSlide].service}.<br />Assista ao Treino
            </p>
          </div>

          {/* Right: stats */}
          <div className="hidden md:flex items-start gap-8">
            <div className="text-right">
              <span className="block text-3xl font-black text-white">+500</span>
              <span className="block text-xs uppercase tracking-widest text-white/40 mt-1">Alunos Ativos</span>
            </div>
            <div className="w-px h-10 bg-white/10 self-center" />
            <div className="text-right">
              <span className="block text-3xl font-black text-white">12</span>
              <span className="block text-xs uppercase tracking-widest text-white/40 mt-1">Anos de Mercado</span>
            </div>
            <div className="w-px h-10 bg-white/10 self-center" />
            <div className="text-right">
              <span className="block text-3xl font-black text-emerald-400">3×</span>
              <span className="block text-xs uppercase tracking-widest text-white/40 mt-1">Melhor Academia</span>
            </div>
          </div>
        </div>

        {/* ── BIG TITLE + subtitle — dominant, bottom-left ── */}
        <div className="absolute bottom-20 left-0 right-0 z-20 px-6">
          {/* Main title */}
          <h1
            key={currentSlide}
            className="text-[clamp(72px,12vw,160px)] leading-[0.88] font-black tracking-tighter text-white animate-slide-up drop-shadow-2xl pointer-events-none"
            dangerouslySetInnerHTML={{ __html: slides[currentSlide].title }}
          />

          {/* Subtitle — below the title, left-aligned, max 50% width */}
          <p
            key={`sub-${currentSlide}`}
            className="mt-6 text-sm md:text-base leading-relaxed text-white/60 max-w-lg animate-slide-up-delay"
          >
            {slides[currentSlide].subtitle}
          </p>
        </div>

        {/* ── Bottom strip ── */}
        <div className="absolute bottom-0 left-0 right-0 z-30 flex items-center h-14 bg-neutral-950/80 backdrop-blur-sm border-t border-white/5">

          {/* Indicators */}
          <div className="flex items-center gap-1 px-6 border-r border-white/10 h-full">
            {slides.map((_, index) => (
              <button
                key={index}
                onClick={() => handleIndicatorClick(index)}
                aria-label={`Slide ${index + 1}`}
                className="flex items-center h-full px-1.5 group cursor-pointer"
              >
                <span
                  className="relative block h-0.75 rounded-full overflow-hidden transition-all duration-300 bg-white/20 group-hover:bg-white/40"
                  style={{ width: currentSlide === index ? "52px" : "18px" }}
                >
                  {currentSlide === index && (
                    <span
                      key={currentSlide}
                      className="absolute inset-y-0 left-0 bg-emerald-500 rounded-full"
                      style={{ animation: `progress-fill ${SLIDE_DURATION}ms linear both` }}
                    />
                  )}
                </span>
              </button>
            ))}
          </div>

          {/* Links */}
          <div className="flex items-center ml-auto text-white">
            <a href="#" className="px-6 font-bold uppercase tracking-widest text-xs flex items-center h-14 hover:text-emerald-400 transition-colors border-r border-white/10">
              Explore o Treino <span className="ml-2">&raquo;</span>
            </a>
            <div className="px-6 flex items-center h-14 font-mono text-xs tracking-widest text-white/50">
              LIGUE: <span className="ml-2 font-bold text-white/90 hover:text-emerald-400 cursor-pointer transition-colors">+55 11 99999-9999</span>
            </div>
          </div>
        </div>

      </section>
    </>
  );
}
