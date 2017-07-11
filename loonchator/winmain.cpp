#pragma comment(lib, "user32")

#include <windows.h>

#include <algorithm>
#include <sstream>
#include <string>
#include <vector>

class Exception {
 public:
  virtual ~Exception() {}
  virtual std::string message() const = 0;
};

class StrException : public Exception {
 public:
  explicit StrException(const std::string& str) : str_(str) {}
  std::string message() const override { return str_; }

 private:
  std::string str_;
};

class WinException : public Exception {
 public:
  WinException() : code_(GetLastError()) {}
  explicit WinException(DWORD code) : code_(code) {}
  std::string message() const override {
    std::ostringstream ss;
    ss << "Windows error " << code_;
    return ss.str();
  }

 private:
  const DWORD code_;
  std::string message_;
};

std::string GetExecutableFilename() {
  std::vector<char> buffer(1024);

  for (;;) {
    DWORD res = GetModuleFileName(0, &buffer[0], buffer.size());
    if (res < buffer.size()) {
      return {buffer.begin(), buffer.begin() + res};
    }
    if (GetLastError() == ERROR_INSUFFICIENT_BUFFER) {
      buffer.resize(buffer.size() * 2);
      continue;
    }
    throw WinException(GetLastError());
  }
}

void MsgBox(const std::string& message) {
  MessageBox(0, message.data(), nullptr, MB_OK);
}

std::vector<std::string> StringSplit(const std::string& str, char c) {
  std::vector<std::string> res;
  auto iter = str.begin();
  while (iter != str.end()) {
    auto new_iter = std::find(iter, str.end(), c);
    res.emplace_back(iter, new_iter);
    iter = new_iter;
    if (iter != str.end()) ++iter;
  }
  if (iter != str.end()) res.emplace_back(iter, str.end());
  return res;
}

std::pair<std::string, std::string> Partition(const std::string& str, char c) {
  auto iter = std::find(str.begin(), str.end(), c);
  if (iter == str.end()) {
    return {str, std::string()};
  }
  return {{str.begin(), iter}, {iter + 1, str.end()}};
}

std::pair<std::string, std::string> PartitionRight(const std::string& str,
                                                   char c) {
  auto iter = std::find(str.rbegin(), str.rend(), c);
  if (iter == str.rend()) {
    return {str, std::string()};
  }
  return {{str.begin(), iter.base() - 1}, {iter.base(), str.end()}};
}

class Version {
 public:
  Version() {}
  explicit Version(const std::string& version_str) {
    auto version_and_suffix = Partition(version_str, '-');
    suffix_ = version_and_suffix.second;
    auto components = StringSplit(version_and_suffix.first, '.');
    if (components.size() > 3 || components.empty())
      throw StrException("Непонятная строка с версией: " + version_str);
    major_ = std::stoi(components[0]);
    if (components.size() == 1) return;
    minor_ = std::stoi(components[1]);
    if (components.size() == 2) return;
    minor_ = std::stoi(components[2]);
  }
private:
  int major_ = 0;
  int minor_ = 0;
  int patch_ = 0;
  std::string suffix_;
};

class VersionedPackage {
 public:
  explicit VersionedPackage(const std::string& val) {
    auto package_and_version = PartitionRight(val, '~');
    if (package_and_version.second.empty())
      throw StrException("Не похоже на имя пакета: " + val);
    package_ = package_and_version.first;
    version_ = Version(package_and_version.second);
  }

  const std::string& Package() const { return package_; }

 private:
  std::string package_;
  Version version_;
};

bool IsInstalled() {
  try {
    auto path = StringSplit(GetExecutableFilename(), '\\');
    auto own_package = VersionedPackage(path[path.size() - 2]);
    if (own_package.Package() != "loonchator") return false;
  } catch (...) {
    return false;
  }
  return true;
}

int CALLBACK WinMain(_In_ HINSTANCE hInstance, _In_ HINSTANCE hPrevInstance,
                     _In_ LPSTR lpCmdLine, _In_ int nCmdShow) {

  if (IsInstalled()) {
    MsgBox("Yes!");
  } else {
    MsgBox("No!");
  }
  return 0;
}