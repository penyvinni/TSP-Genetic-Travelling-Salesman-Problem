# include <stdio.h>
# include <stdlib.h>
# include <math.h>
# include <vector>
# include <cstdlib> // Add this line
#include <random>
using namespace std;

typedef struct
{
	double x;
	double y;
}Point;

typedef vector<int> Route;

std::random_device rd;
std::default_random_engine generator(rd());

double	getDistance(Point a,Point b)
{
	return sqrt(pow(a.x-b.x,2.0)+pow(a.y-b.y,2.0));
}

void	makeRoute(Route &route)
{
	int i;
	for(i=0;i<route.size();i++) route[i]=i+1;
	for(i=0;i<route.size();i++)
	{
		int t=rand() % route.size();
		int v=route[t];
		route[t]=route[i];
		route[i]=v;
	}
}

void	printRoute(Route route)
{
	int i;
	for(i=0;i<route.size()-1;i++)
		printf("%d->",route[i]);
	printf("%d\n",route[route.size()-1]);
}

void	swapRoutes(Route &a,Route &b)
{
	for(int i=0;i<a.size();i++)
	{
		int itemp=a[i];
		a[i]=b[i];
		b[i]=itemp;
	}
}

double	fitnessRoute(Route route,vector<Point> location)
{
	double value=0.0;
	for(int i=0;i<route.size()-1;i++)
		value+=getDistance(location[route[i]],location[route[i+1]]);
	return value;
}

void	calculateRoutes(vector<Route> genome,vector<Point> location,vector<double> &fitness)
{
	for(int i=0;i<genome.size();i++)
		fitness[i]=fitnessRoute(genome[i],location);
}

void	sortRoutes(vector<Route> &genome,vector<double> &fitness)
{
	for(int i=0;i<genome.size();i++)
	{
		for(int j=0;j<genome.size()-1;j++)
		{
			if(fitness[j+1]<fitness[j])
			{
				double dtemp=fitness[j];
				fitness[j]=fitness[j+1];
				fitness[j+1]=dtemp;
				swapRoutes(genome[j],genome[j+1]);
			}
		}
	}
}

void	mutateRoute(Route &route,int pos)
{
	int t=route[pos];
	int random_pos=rand() % route.size();
	route[pos]=route[random_pos];
	route[random_pos]=t;
}

int	inRoute(Route route,int pos,int element)
{
	for(int i=0;i<=pos;i++) if(route[i]==element) return 1;
	return 0;
}

void	makeChild(Route &child,Route parent1,Route parent2)
{
	//UNIFORM CROSSOVER
	child.resize(parent1.size());
	for(int i=0;i<child.size();i++)
	{
		do
		{
			int t1=rand() % child.size();
			int t2=rand() % child.size();
			if(!inRoute(child,i-1,parent1[t1]))
			{
				child[i]=parent1[t1];
				break;
			}
			else
			if(!inRoute(child,i-1,parent2[t2]))
			{
				child[i]=parent2[t2];
				break;
			}
		}while(1);	
	}
}

void	crossoverRoutes(vector<Route> &genome,vector<double> &fitness)
{
	const int tournament_size=4;
	const double pc=0.99; //crossover probability
	vector<Route> children;
	children.resize((int)(genome.size()*pc));
	for(int i=0;i<children.size();i++) children.resize(genome[0].size());
	int count_children=0;
	do
	{
		//tournament selection
		int parent[2];
		for(int i=0;i<2;i++)
		{
			int min_pos=0;
			double min_fitness=1e+100;
			for(int j=0;j<tournament_size;j++)
			{
				int r=rand() % genome.size();
				if(fitness[r]<min_fitness)
				{
					min_pos=r;
					min_fitness=fitness[r];
				}
			}
			parent[i]=min_pos;
		}
		makeChild(children[count_children],genome[parent[0]],genome[parent[1]]);
		count_children++;
		if(count_children==children.size()) break;
		makeChild(children[count_children],genome[parent[0]],genome[parent[1]]);
		count_children++;
	}while(count_children!=children.size());

	//replace the worst chromosomes
	for(int i=0;i<count_children;i++)
	{
		genome[genome.size()-i-1]=children[i];
	}
}

void	mutateRoutes(vector<Route> &genome)
{
	double pm=1.0/genome[0].size(); //mutation rate
	for(int  i=1;i<genome.size();i++) //do not change the first chromosome
	{
		for(int j=0;j<genome[i].size();j++)
		{
			//double r=srand(0);
			//if(r<pm) mutateRoute(genome[i],j);
			std::uniform_real_distribution<double> distribution(0.0, 1.0);
			double r = distribution(generator);
			if (r < pm) mutateRoute(genome[i], j);
		}
	}
}


int main(int argc,char **argv)
{
	vector<Point> location;
	//MAXIMUM COORDINATES FOR THE CITIES
	double maxx,minx,maxy,miny;
	int	N;
	int 	i;
	int 	genome_count;
	vector<Route> genome;
	vector<double> fitness;
	int	generation;
	int maxgenerations;
	std::uniform_real_distribution<double> distribution(0.0, 1.0);
	srand(0);
	srand(0);
	// srand48(0);

	do
	{
		printf("HOW MANY CITIES ?");
		scanf("%d",&N);
	}while(N<=0);
	location.resize(N);	
	do
	{
		printf("ENTER MINX ?");
		scanf("%lf",&minx);
		printf("ENTER MAXX ?");
		scanf("%lf",&maxx);
	}while(maxx<minx);
	do
	{
		printf("ENTER MINY ?");
		scanf("%lf",&miny);
		printf("ENTER MAXY ?");
		scanf("%lf",&maxy);
	}while(maxy<miny);
	std::random_device rd;
	std::default_random_engine generator(rd());
	std::uniform_real_distribution<double> distribution_x(minx, maxx);
	std::uniform_real_distribution<double> distribution_y(miny, maxy);
	for(i=0;i<location.size();i++)
	{
		//location[i].x=minx+(maxx-minx)*drand48();
		//location[i].y=miny+(maxy-miny)*drand48();
    	location[i].x = distribution_x(generator);
    	location[i].y = distribution_y(generator);
	}

	//INITIALIZATION OF THE CHROMOSOMES
	do
	{
		printf("HOW MANY ROUTES FOR THE POPULATION ?");
		scanf("%d",&genome_count);
	}while(genome_count<=0);
	genome.resize(genome_count);
	fitness.resize(genome_count);
	for(int i=0;i<genome_count;i++) 
	{
		genome[i].resize(N);
		makeRoute(genome[i]);
	}
	do
	{
		printf("HOW MANY GENERATIONS ?");
		scanf("%d",&maxgenerations);
	}while(maxgenerations<=0);
	//THE MAIN LOOP OF THE ALGORITHM
	double mean_best=0.0;
	double sx1=0.0,sx2=0.0;
	for(generation=1;generation<=maxgenerations;generation++)
	{
		calculateRoutes(genome,location,fitness);
		sortRoutes(genome,fitness);
		mean_best+=fitness[0];
		sx1+=(fitness[0]);
		sx2+=(fitness[0])*(fitness[0]);
		printf("generation: %d best route so far  ",generation);
		printRoute(genome[0]);
		printf("fitness = %lf \n",fitness[0]);
		printf("MEAN OF BEST FITNESS %lf \n",mean_best/generation);
		printf("STD  OF BEST FITNESS %lf \n",sx2/generation-sx1/generation*sx1/generation);
		crossoverRoutes(genome,fitness);
		mutateRoutes(genome);
	}

	return 0;
}
