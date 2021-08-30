#define uint8 unsigned short
#define int32 int

typedef enum {
	Shop,
	Home,
	Login,
	Order
} MyStm_e;

MyStm_e st;

int32 button3 = 0;
int32 button2 = 0;
int32 button1 = 0;
int32 button4 = 0;

static uint8 t829() {
	return button1 == 1;
}

static uint8 t380() {
	return button3 == 1;
}

static uint8 t605() {
	return button4 == 1;
}

static uint8 t754() {
	return button2 == 1;
}

static uint8 t273() {
	return button2 == 1;
}

static uint8 STM_IMPLEMENTATION() {
	switch (st) {
		case Shop:
			if (t380()) {
				st=Order;
			}
			break;
		case Home:
			if (t829()) {
				st=Login;
			}
			if (t754()) {
				st=Shop;
			}
			break;
		case Login:
			if (t273()) {
				st=Shop;
			}
			break;
		case Order:
			if (t605()) {
				st=Home;
			}
			break;
	}
}

int main() {
	return 0;
}