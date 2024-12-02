#include <iostream>
#include <string>
#include "std_lib.h"
using namespace std;

typedef struct Timer {
	int time;
	void init(int time_) {
		time = time_;
	}
	void start() {
		while (time >= 0) {
			string str_time = icasts(time);
			print(str_time);
			time = time - 1;
			wait(1000);
		}
	}
} Timer;
typedef struct Happy {
	void init() {
		for (int i = 0; i < 10; i = i + 1) {
			if (i == 5) {
				print("Sad");
			}
			else {
				print("Happy");
			}
			wait(1000);
		}
	}
} Happy;
int main() {
	string t = input("Enter time: ");
	int t_int = scasti(t);
	Timer timer;
	timer.init(t_int);
	timer.start();
	Happy happy;
	happy.init();
	return 0;
}