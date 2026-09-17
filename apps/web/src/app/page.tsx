import Navbar from "@/components/Navbar";
import HeroSection from "@/components/HeroSection";
import FeaturesCards from "@/components/FeaturesCards";
import AlternatingFeature from "@/components/AlternatingFeature";
import GalleryAndCTA from "@/components/GalleryAndCTA";
import CoachesSection from "@/components/CoachesSection";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#cdcdcd]">
      <Navbar />
      <HeroSection />
      <FeaturesCards />
      
      {/* "More Than a Gym" Header (before the features) */}
      <section className="bg-[#cdcdcd] pt-24 pb-12 flex flex-col items-center text-black">
        <span className="text-xs font-bold uppercase tracking-widest text-neutral-500 mb-6">( PROJETADO PARA PERFORMANCE )</span>
        <h2 className="text-4xl md:text-5xl font-medium tracking-tight text-center">
          Mais que uma Academia — Um Espaço<br/>Construído para o Progresso
        </h2>
      </section>

      {/* The 01, 02, 03 Sections */}
      <AlternatingFeature 
        number="01"
        title="Treinamento Funcional"
        description="Um espaço especializado para treinamento funcional, mobilidade, alongamento e recuperação. Inclui ferramentas para cross training, equilíbrio e flexibilidade para ajudar a reduzir o risco de lesões e melhorar a qualidade do movimento."
        imageUrl="https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?q=80&w=2070&auto=format&fit=crop"
        reverse={false}
      />

      <AlternatingFeature 
        number="02"
        title="Área de Cardio"
        description="Uma área de cardio moderna equipada com esteiras, bicicletas, remos e elípticos. Projetada para melhorar a resistência cardiovascular, auxiliar na perda de gordura e aumentar o vigor geral em um ambiente motivador e de alta energia."
        imageUrl="https://images.unsplash.com/photo-1538805060514-97d9cc17730c?q=80&w=2187&auto=format&fit=crop"
        reverse={true}
      />

      <AlternatingFeature 
        number="03"
        title="Fitness & Pilates"
        description="Uma área de força e fitness totalmente equipada com pesos livres, máquinas de resistência e equipamentos funcionais. Perfeita para construção muscular, aumento de força e melhoria da performance de corpo inteiro para todos os níveis."
        imageUrl="https://images.unsplash.com/photo-1518611012118-696072aa579a?q=80&w=2070&auto=format&fit=crop"
        reverse={false}
      />

      <GalleryAndCTA />
      <CoachesSection />
      <Footer />
    </main>
  );
}
