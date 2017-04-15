#include "bits/stdc++.h"
using namespace std;
int main()
{
	freopen("datasec.csv","w+",stdout);
	int month=-1;
	int day=0;
	int count=0;
	printf("SNo,Time\n");
	for (int i = 0; i < 200; ++i)
	{
		float LO=-0.5,HI=0.5;
		float r3 = LO + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(HI-LO)));
		printf("%d,%f\n",++day,1+r3);

	}
	/*

	for (int i = 0; i < 20; ++i)
	{
		printf("%d,%f\n",++day,1.0);
	}
	*/
	return 0;
}