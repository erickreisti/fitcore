interface AlternatingFeatureProps {
  number: string;
  title: string;
  description: string;
  imageUrl: string;
  reverse?: boolean;
}

export default function AlternatingFeature({ number, title, description, imageUrl, reverse = false }: AlternatingFeatureProps) {
  return (
    <section className="bg-[#cdcdcd] w-full py-16 flex justify-center">
      <div className={`container max-w-6xl mx-auto flex flex-col ${reverse ? 'md:flex-row-reverse' : 'md:flex-row'} bg-black overflow-hidden shadow-2xl min-h-125`}>
        
        {/* Text Side */}
        <div className="w-full md:w-1/2 p-16 flex flex-col justify-center relative overflow-hidden bg-linear-to-br from-[#1c1c1c] to-black">
          {/* Big Number Background */}
          <div className="absolute -top-10 -left-10 text-[300px] font-black text-transparent opacity-10 pointer-events-none select-none leading-none"
               style={{ WebkitTextStroke: "2px rgba(255,255,255,1)" }}>
            {number}
          </div>
          
          <div className="relative z-10">
            <span className="text-gray-400 font-mono text-sm tracking-widest mb-10 block">{number}</span>
            <h2 className="text-4xl font-bold text-white mb-6">{title}</h2>
            <p className="text-gray-400 text-sm leading-relaxed mb-10 max-w-md">
              {description}
            </p>
            <a href="#" className="inline-flex items-center bg-white text-black px-6 py-3 text-xs font-bold uppercase tracking-widest hover:bg-emerald-500 hover:text-white transition-colors">
              Explore More <span className="ml-2 text-lg leading-none">&raquo;</span>
            </a>
          </div>
        </div>

        {/* Image Side */}
        <div className="w-full md:w-1/2 relative min-h-75 md:min-h-full">
          <div 
            className="absolute inset-0 bg-cover bg-center"
            style={{ backgroundImage: `url('${imageUrl}')` }}
          />
          {/* Subtle gradient to blend the edge */}
          <div className={`absolute inset-y-0 ${reverse ? 'right-0 bg-linear-to-l' : 'left-0 bg-linear-to-r'} from-black/80 to-transparent w-24`} />
        </div>

      </div>
    </section>
  );
}
