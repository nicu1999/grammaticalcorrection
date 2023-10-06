CXX = g++
CXXFLAGS = -std=c++11

TARGET1 = main_mod_del
TARGET2 = main_add
TARGET3 = main_test
SRCS1 = main_mod_del.cpp
SRCS2 = main_add.cpp
SRCS3 = main_test.cpp

.PHONY: all clean

all: $(TARGET1) $(TARGET2) $(TARGET3)

$(TARGET1): $(SRCS1)
	$(CXX) $(CXXFLAGS) $^ -o $@

$(TARGET2): $(SRCS2)
	$(CXX) $(CXXFLAGS) $^ -o $@

$(TARGET3): $(SRCS3)
	$(CXX) $(CXXFLAGS) $^ -o $@

clean:
	rm -f $(TARGET1) $(TARGET2) $(TARGET3)