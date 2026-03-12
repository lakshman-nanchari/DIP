export default function DashboardSkeleton() {

  return (
    <div className="animate-pulse space-y-6">

      <div className="grid grid-cols-4 gap-6">

        <div className="bg-stone-200 h-24 rounded-xl"></div>
        <div className="bg-stone-200 h-24 rounded-xl"></div>
        <div className="bg-stone-200 h-24 rounded-xl"></div>
        <div className="bg-stone-200 h-24 rounded-xl"></div>

      </div>

      <div className="bg-stone-200 h-72 rounded-xl"></div>

      <div className="bg-stone-200 h-72 rounded-xl"></div>

    </div>
  );
}